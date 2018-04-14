//
//  UploadVideoViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta on 4/5/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import Alamofire
import MobileCoreServices
import FirebaseAuth

class UploadVideoViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    
    let imagePickerController = UIImagePickerController()
    //    var videoURL: URL?
    var uid: Any?
    
    @IBOutlet weak var displayImage: UIImageView!
    @IBOutlet weak var videoTitleBox: UITextField!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        //        Auth.auth().addStateDidChangeListener { (auth, user) in
        //            self.uid = user?.uid
        //        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func uploadVideoBtn(_ sender: Any) {
        let title: String = videoTitleBox.text!
        let parameters: Parameters = [
            //            "user_id": uid!,
            "user_id": "1234567",
            "title": title,
            //            "src": videoURL!
            "src": "videoURL!"
        ]
        
        //        Alamofire.request("http://localhost:5000/api/post/video", method: .post, parameters: parameters, encoding: JSONEncoding.default)
        
        //        Alamofire.upload(videoURL!, to: "http://localhost:5000/api/post/video").responseJSON { response in
        //            debugPrint(response)
        //        }
        
    }
    
    @IBAction func cancelUploadBtn(_ sender: UIButton) {
        self.dismiss(animated: true, completion: nil)
    }
    
    @IBAction func selectFilesBtn(_ sender: UIButton) {
        
        AttachmentHandler.shared.showAttachmentActionSheet(vc: self)
        AttachmentHandler.shared.imagePickedBlock = { (image) in
            /* get your image here */
            print(image)
            self.displayImage.image = image
            
            
            
            
        }
        
        // video params must be uploaded to the server along with the title and user_id.
        AttachmentHandler.shared.videoPickedBlock = { (video) in
            print("Video is here: \(video)")
            let videoURL = video
            
            let title = self.videoTitleBox.text!
            
            let parameters =  [
                "title" : title
            ]
            
            Alamofire.upload(multipartFormData: { MultipartFormData in
                
                //mp4 video
                //MultipartFormData.append(videoURL.absoluteURL!, withName: "file", fileName: filename, mimeType: "video/mp4")
                MultipartFormData.append(videoURL.absoluteURL!, withName: "file")
                
                for (key, value) in parameters {
                    MultipartFormData.append(value.data(using: String.Encoding.utf8)!, withName: key)
                }
            },to:"http://127.0.0.1:5000/api/post/video"){ (result) in
                switch result {
                case .success(let upload, _, _):
                    upload.uploadProgress(closure: { (progress) in
                        print("Uploading Percent: \(progress.fractionCompleted)")
                        self.dismiss(animated: true, completion: nil)
                    })
                    upload.responseJSON { response in
                        print("Result: ",response.result.value ?? String())
                        print("Data: ",response.data ?? NSData())
                    }
                case .failure(let encodingError):
                    print(encodingError)
                }
            }
            
        }
        
    }
    
}


