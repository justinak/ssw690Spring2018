//
//  VideoViewController.swift
//  Stevens Social
//
//  Created by Michael Kim on 3/26/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import MediaPlayer
import AVFoundation
import AVKit


import UIKit
import youtube_ios_player_helper

class ViewController: UIViewController, YTPlayerViewDelegate {
    @IBOutlet weak var playerView: YTPlayerView!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        playerView.delegate = self
        
        let playerVars = ["playsinline": 1] // 0: will play video in fullscreen
        self.playerView.loadWithVideoId("youtubeId", playerVars: playerVars)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}


