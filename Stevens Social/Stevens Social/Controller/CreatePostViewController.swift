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
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Allows us to use the delegate
        postBody.delegate = self
        
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

            //UserID
            let userEmail = Auth.auth().currentUser!.email
        
            //declare parameter as a dictionary which contains string as key and value combination. considering inputs are valid
        let parameters = ["email": userEmail, "postBody": postBody!.text] as! Dictionary<String, String>
        
            //create the url with URL
            let url = URL(string: "http://127.0.0.1:5000/api/NewPost")!
        
            //create the session object
            let session = URLSession.shared
        
            //now create the URLRequest object using the url object
            var request = URLRequest(url: url)
            request.httpMethod = "POST" //set http method as POST
        
            do {
                request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: .prettyPrinted) // pass dictionary to nsdata object and set it as request body
                
            } catch let error {
                print(error.localizedDescription)
            }
        
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
        
            //create dataTask using the session object to send data to the server
            let task = session.dataTask(with: request as URLRequest, completionHandler: { data, response, error in
                
                guard error == nil else {
                    return
                }
                
                guard let data = data else {
                    return
                }
                
                do {
                    //create json object from data
                    if let json = try JSONSerialization.jsonObject(with: data, options: .mutableContainers) as? [String: Any] {
                        print(json)
                        // handle json...
                    }
                    
                } catch let error {
                    print(error.localizedDescription)
                }
            })
            task.resume()
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

