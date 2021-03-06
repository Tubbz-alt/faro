'''
MIT License

Copyright 2019 Oak Ridge National Laboratory

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Created on October 3, 2019

@author: srinivasn1
@ORNL
'''

import faro
import os
import faro.proto.proto_types as pt 
import faro.proto.face_service_pb2 as fsd
import numpy as np
import pyvision as pv
from faro.FaceGallery import SearchableGalleryWorker
 
def getGalleryWorker(options):
    print("Arcface: Creating indexed gallery worker...")
    return SearchableGalleryWorker(options,fsd.NEG_DOT)

class ArcfaceFaceWorker(faro.FaceWorker):
    '''
    classdocs
    '''

    def __init__(self, options):
        '''
        Constructor
        '''
        import insightface
        os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = '0'
        kwargs = {'root':os.path.join(options.storage_dir,'models')}
        #load Retina face model
        self.detector = insightface.model_zoo.get_model('retinaface_r50_v1',**kwargs)
        if options.gpuid == -1:
            ctx_id = -1
        else:
            ctx_id = int(options.gpuid)
        #self.detector.rac = 'net5'
        #set ctx_id to a gpu a predefined gpu value
        self.detector.prepare(ctx_id, nms=0.4)
        # load arcface FR model
        self.fr_model = insightface.model_zoo.get_model('arcface_r100_v1',**kwargs)
        
        self.fr_model.prepare(ctx_id) 
        self.preprocess = insightface.utils.face_align
        print("ArcFace Models Loaded.")

        
    def detect(self,img,face_records,options):
        '''Run a face detector and return rectangles.'''
        #print('Running Face Detector For ArchFace')
        img = img[:,:,::-1] #convert from rgb to bgr . There is a reordering from bgr to RGB internally in the detector code.
        dets, lpts = self.detector.detect(img, threshold=options.threshold, scale=1)
        #print('Number of detections ', dets.shape[0])
        # Now process each face we found and add a face to the records list.
        for idx in range(0,dets.shape[0]):
            face_record = face_records.face_records.add()
            try: # todo: this seems to be different depending on mxnet version
                face_record.detection.score = dets[idx,-1:]
            except:
                face_record.detection.score = dets[idx,-1:][0]
            ulx, uly, lrx, lry = dets[idx,:-1]        
            #create_square_bbox = np.amax(abs(lrx-ulx) , abs(lry-uly))
            face_record.detection.location.CopyFrom(pt.rect_val2proto(ulx, uly, abs(lrx-ulx) , abs(lry-uly)))
            face_record.detection.detection_id = idx
            face_record.detection.detection_class = "FACE_%d"%idx
            #lmark = face_record.landmarks.add()
            lmarkloc = lpts[idx]
            for ldx in range(0,lmarkloc.shape[0]):
                lmark = face_record.landmarks.add()
                lmark.landmark_id = "point_%02d"%ldx
                lmark.location.x = lmarkloc[ldx][0]
                lmark.location.y = lmarkloc[ldx][1]

        if options.best:
            face_records.face_records.sort(key = lambda x: -x.detection.score)
            
            while len(face_records.face_records) > 1:
                del face_records.face_records[-1]
            
        #print('Done Running Face Detector For ArchFace')
    
    def locate(self,img,face_records,options):
        '''Locate facial features.'''
        pass #the 5 landmarks points that retina face detects are stored during detection
        
        
    def align(self,image,face_records):
        '''Align the images to a standard size and orientation to allow 
        recognition.'''
        pass # Not needed for this algorithm.
            
    def extract(self,img,face_records):
        '''Extract a template that allows the face to be matched.'''
        # Compute the 512D vector that describes the face in img identified by
        #shape.
        #print(type(img),img.shape)
        img = img[:,:,::-1] #convert from rgb to bgr. There is BGRtoRGB conversion in get_embedding

        for face_record in face_records.face_records:
            #print(face_record)
            if face_record.detection.score != -1:
                landmarks = np.zeros((5,2),dtype=np.float)
                for i in range(0,len(face_record.landmarks)):
                        vals = face_record.landmarks[i]
                        landmarks[i,0] = vals.location.x
                        landmarks[i,1] = vals.location.y
 
                _img = self.preprocess.norm_crop(img, landmark = landmarks)
                #print(_img.shape)            
                embedding = self.fr_model.get_embedding(_img).flatten()
                embedding_norm = np.linalg.norm(embedding)
                normed_embedding = embedding / embedding_norm
                #print(normed_embedding.shape)

                # Extract view
                x,y,w,h = pt.rect_proto2pv(face_record.detection.location).asTuple()
                cx,cy = x+0.5*w,y+0.5*h
                tmp = 1.5*max(w,h)
                cw,ch = tmp,tmp
                crop = pv.AffineFromRect(pv.CenteredRect(cx,cy,cw,ch),(256,256))
                #print (x,y,w,h,cx,cy,cw,ch,crop)
                pvim = pv.Image(img[:,:,::-1]) # convert rgb to bgr
                pvim = crop(pvim)
                view = pt.image_pv2proto(pvim)
                face_record.view.CopyFrom(view)

            else:
                normed_embedding = np.zeros(512,dtype=float)
            
            face_record.template.data.CopyFrom(pt.vector_np2proto(normed_embedding))

                
    def scoreType(self):
        '''Return the method used to create a score from the template.
        
        By default server computation is required.
        
        SCORE_L1, SCORE_L2, SCORE_DOT, SCORE_SERVER
        '''
        return fsd.NEG_DOT
    
    def status(self):
        '''Return a simple status message.'''
        status_message = fsd.FaceServiceInfo()
        status_message.status = fsd.READY
        status_message.detection_support = True
        status_message.extract_support = True
        status_message.score_support = True
        status_message.score_type = self.scoreType()
        status_message.detection_threshold = self.recommendedDetectionThreshold()
        status_message.match_threshold = self.recommendedScoreThreshold()
        status_message.algorithm = "ArcFace-model arcface_r100_v1"

        
        return status_message
        

    def recommendedDetectionThreshold(self):
        
        return 0.5

    def recommendedScoreThreshold(self,far=-1):
       
        '''
        Arcface does not provide a match threshold
        '''
         
        return -0.42838144


