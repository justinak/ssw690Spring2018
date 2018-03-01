//
//  ViewController.swift
//  Stevens Social
//
//  Created by Michael Kim on 2/28/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit

var username = ""

class ViewController: UIViewController {

    @IBOutlet weak var UserName: UITextField!
    @IBOutlet weak var UserID: UITextField!
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
        if (UserName.text != ""){
            username = UserName.text!
            performSegue(withIdentifier: "segue", sender: self)
        }
    }
}

