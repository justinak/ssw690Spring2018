//
//  CreatePostViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta on 3/14/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import CoreData
import FirebaseAuth

class CreatePostViewController: UIViewController, UITextFieldDelegate, UITableViewDelegate {
    

    @IBOutlet var postBody: UITextField!
    
    //PersistentContainer : Creates and Returns a container
    var context = (UIApplication.shared.delegate as! AppDelegate).persistentContainer.viewContext
//    var uid: String?
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Allows us to use the delegate
        postBody.delegate = self
        
//        Auth.auth().addStateDidChangeListener { (auth, user) in
//            self.uid = user?.uid
//        }
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func cancelPost(_ sender: UIButton) {
        self.dismiss(animated: true, completion: nil)
    }
    
    
    @IBAction func confirmPost(_ sender: UIButton) {
        
        if postBody?.text != ""{
            //Putting attribute value into newPost from textfield
           
            let newPost = NSEntityDescription.insertNewObject(forEntityName: "Post", into: context)
//            print("uid here: " + uid!)
//            newPost.setValue(uid, forKey: "userID")
            newPost.setValue(self.postBody!.text, forKey: "postBody")
           
            do{
                try context.save()
                performSegue(withIdentifier: "postSuccess", sender: self)
            }catch{
                print(error)
            }
        }else{
            print("Please enter text in the Post Box!")
        }
        
//        let myAPI = API(customRoute: "http://127.0.0.1:5000/api/NewPost", customMethod: "POST")
//        myAPI.sendRequest(parameters: ["uuid": uid!, "postBody": self.postBody!.text!])
    }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */
}

