//
//  WelcomeViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta on 3/4/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit

class WelcomeViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
<<<<<<< HEAD:Stevens Social/Stevens Social/MainScreenViewController.swift
        
=======

>>>>>>> b3b87a8bb5c0ac8bd53ea8b14513fab22b5f0e4a:Stevens Social/Stevens Social/WelcomeViewController.swift
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func ProfileButton(_ sender: Any) {
        performSegue(withIdentifier: "ProfileSegue", sender: self)
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
