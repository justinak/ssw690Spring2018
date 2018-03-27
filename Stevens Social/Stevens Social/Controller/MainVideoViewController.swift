//
//  MainVideoViewController.swift
//  Stevens Social
//
//  Created by Michael Kim on 3/26/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit

class MainVideoViewController: UIViewController {

  
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func PlayVideoBtn(_ sender: Any) {
        performSegue(withIdentifier: "watchVideo", sender: self)
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
