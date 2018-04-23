//
//  CreateExpViewController.swift
//  Stevens Social
//
//  Created by Michael Kim on 4/14/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import Firebase

class CreateExpViewController: UIViewController {

    @IBOutlet weak var expPost: UITextField!
    
    let ExpViewCont = ExperienceViewController()
    
    let userID = Auth.auth().currentUser!.uid
    
    @IBAction func postButton(_ sender: Any) {
        if expPost?.text != "" {
            let myAPI = API(customRoute: "http://127.0.0.1:5000/api/new/experiences", customMethod: "POST")
            myAPI.sendRequest(parameters: ["experience": self.expPost!.text!, "userid": userID])
            
            let expAPI = API(customRoute: "http://127.0.0.1:5000/api/get/experiences", customMethod: "GET")
            expAPI.sendRequest(parameters: [:])
            
        } else {
            print("Please enter experience in the Post Box!")
        }
        self.dismiss(animated: true, completion: nil)
    }
    
    @IBAction func cancelButton(_ sender: Any) {
        self.dismiss(animated: true, completion: nil)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}
