//
//  ViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta, Michael Kim on 2/28/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import Firebase


class LoginViewController: UIViewController {

    @IBOutlet weak var UserName: UITextField!
    @IBOutlet weak var UserPassword: UITextField!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func LoginClick(_ sender: Any) {
        Auth.auth().signIn(withEmail: UserName.text!, password: UserPassword.text!) { (user, error) in
            if error != nil {
                print(error!)
                let alert = UIAlertController(title: "Incorrect email or password", message: "Please enter a valid stevens.edu email", preferredStyle: .alert)
                alert.addAction(UIAlertAction(title: NSLocalizedString("OK", comment: "Default action"), style: .`default`, handler: { _ in
                    NSLog("The \"OK\" alert occured.")
                }))
                self.present(alert, animated: true, completion: nil)
            } else if (user?.isEmailVerified)! {
                print("Email is verified")
                self.performSegue(withIdentifier: "goToHome", sender: self)
            } else {
                print("login successful")
                let alert = UIAlertController(title: "Email not verified", message: "Please verify your \(user?.email ?? self.UserName.text!) email address", preferredStyle: .alert)
                alert.addAction(UIAlertAction(title: NSLocalizedString("OK", comment: "Default action"), style: .`default`, handler: { _ in
                    NSLog("The \"OK\" alert occured.")
                }))
                self.present(alert, animated: true, completion: nil)

            }
            let _id = user?.uid
            let email = user?.email
            let parameters = ["id": _id, "email": email] as! Dictionary<String, String>
            
            //create the url with URL
            let url = URL(string: "http://127.0.0.1:5000/api/new/users")!
            
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
    }
}

