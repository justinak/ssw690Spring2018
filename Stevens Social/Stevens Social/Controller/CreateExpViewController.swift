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
            let myAPI = API(customRoute: "https://stevens-social-app.herokuapp.com/api/new/experiences", customMethod: "POST")
            myAPI.sendRequest(parameters: ["experience": self.expPost!.text!, "userid": userID])
            
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
