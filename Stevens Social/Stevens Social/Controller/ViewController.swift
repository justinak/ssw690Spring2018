//
//  ViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta, Michael Kim on 2/28/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit


class ViewController: UIViewController {

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
//            performSegue(withIdentifier: "LoginSegue", sender: self)
        
    }
    
    
}

