//
//  RegisterViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta on 3/5/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import Firebase


class RegisterViewController: UIViewController {

    @IBOutlet weak var emailTextField: UITextField!
    @IBOutlet weak var passwordTextField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    @IBAction func registerPressed(_ sender: AnyObject) {
        
        if self.isValidEmail(email: emailTextField.text!) {
            print("valid email")
            Auth.auth().createUser(withEmail: emailTextField.text!, password: passwordTextField.text!) { (user, error) in
                if error != nil {
                    print(error!)
                    // This should send an error alert
                    let alert = UIAlertController(title: "Incorrect email or password", message: "Please enter a valid stevens.edu", preferredStyle: .alert)
                    alert.addAction(UIAlertAction(title: NSLocalizedString("OK", comment: "Default action"), style: .`default`, handler: { _ in
                        NSLog("The \"OK\" alert occured.")
                    }))
                    self.present(alert, animated: true, completion: nil)
                } else {
                    print("registration success")
                    var uid = user?.uid
                    var email = user?.email
                    let myAPI = API(customRoute: "http://127.0.0.1:5000/api/new/user", customMethod: "POST")
                    myAPI.sendRequest(parameters: ["uuid": uid!, "email": email!])
                    print(myAPI)

                    user?.sendEmailVerification(completion: { (error) in
                        if error != nil {
                            print(error!)
                        } else {
                            print("email verification link being sent")
                            let alert = UIAlertController(title: "Email Confirmation", message: "An email has been sent to \(user?.email ?? self.emailTextField.text)", preferredStyle: .alert)
                            alert.addAction(UIAlertAction(title: NSLocalizedString("OK", comment: "Default action"), style: .`default`, handler: { _ in
                                NSLog("The \"OK\" alert occured.")
                            }))
                            self.present(alert, animated: true, completion: nil)
                        }
                    })
                }
                
            }
        } else {
            print("invalid email")
        }

    }
    
    func isValidEmail(email: String) -> Bool {
        let emailRegex = "^[\\w.+\\-]+@stevens\\.edu$"
        return NSPredicate(format: "SELF MATCHES %@", emailRegex).evaluate(with: email)

    }
    
    

}
