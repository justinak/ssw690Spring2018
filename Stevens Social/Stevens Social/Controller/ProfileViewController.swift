//
//  ProfileViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta on 4/13/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit

class ProfileViewController: UIViewController {

    @IBOutlet var nameHere: UILabel!
    var data = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()
    
        nameHere.text = data
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    

}
