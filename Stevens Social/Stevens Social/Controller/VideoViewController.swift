//
//  VideoViewController.swift
//  Stevens Social
//
//  Created by Michael Kim on 3/26/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit

class VideoViewController: UIViewController {

    @IBOutlet var videoView: UIWebView!
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        
        //Allow Video View to play video back
        videoView.allowsInlineMediaPlayback = true
        
        videoView.loadHTMLString("<iframe width=\"\(videoView.frame.width)\" height=\"\(videoView.frame.height)\" src=\"https://www.youtube.com/embed/g36FwefoGRk?&playsinline=1\" frameborder=\"0\" allowfullscreen></iframe>", baseURL: nil)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
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
