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
        }
//         self.performSegue(withIdentifier: "goToHome", sender: self)
    }
}

