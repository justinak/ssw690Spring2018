//
//  VideoTableViewCell.swift
//  Stevens Social
//
//  Created by Vincent Porta on 3/31/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import AVFoundation


class VideoTableViewCell: UITableViewCell {

    @IBOutlet var videoTitle: UILabel!
    @IBOutlet var videoPoster: UILabel!
    
    @IBOutlet weak var videoPlayerSuperView: UIView!
    
    var avPlayer: AVPlayer?
    var avPlayerLayer: AVPlayerLayer?
    var paused: Bool = false
    
    //This will be called everytime a new value is set on the videoplayer item
    var videoPlayerItem: AVPlayerItem? = nil {
        didSet {
            /*
             If needed, configure player item here before associating it with a player.
             (example: adding outputs, setting text style rules, selecting media options)
             */
            avPlayer?.replaceCurrentItem(with: self.videoPlayerItem)
        }
    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code

        self.setupMoviePlayer()
        
    }
    
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        
        // Configure the view for the selected state
    }
    
    func setupMoviePlayer(){
        self.avPlayer = AVPlayer.init(playerItem: self.videoPlayerItem)
        avPlayerLayer = AVPlayerLayer(player: avPlayer)
        avPlayerLayer?.videoGravity = AVLayerVideoGravity.resizeAspect
        avPlayerLayer?.frame = self.videoPlayerSuperView.bounds
        avPlayer?.volume = 3
        avPlayer?.actionAtItemEnd = .none

//        if UIScreen.main.bounds.width == 375 {
//            let widthRequired = self.frame.size.width - 20
//            avPlayerLayer?.frame = CGRect.init(x: 0, y: 0, width: widthRequired, height: widthRequired/1.78)
//        } else if UIScreen.main.bounds.width == 320 {
//            avPlayerLayer?.frame = CGRect.init(x: 0, y: 0, width: (self.frame.size.height - 120) * 1.78, height: self.frame.size.height - 120)
//        } else {
//            let widthRequired = self.frame.size.width
//            avPlayerLayer?.frame = CGRect.init(x: 0, y: 0, width: widthRequired, height: widthRequired/1.78)
//        }
//        let widthRequired = self.frame.size.width
//        avPlayerLayer?.frame = CGRect.init(x: 0, y: 0, width: widthRequired, height: widthRequired/1.78)
        
        
        self.videoPlayerSuperView.layer.insertSublayer(avPlayerLayer!, at: 0)
        
        // This notification is fired when the video ends, you can handle it in the method.
        NotificationCenter.default.addObserver(self,
                                               selector: #selector(self.playerItemDidReachEnd(notification:)),
                                               name: NSNotification.Name.AVPlayerItemDidPlayToEndTime,
                                               object: avPlayer?.currentItem)
    }
    
    func stopPlayback(){
        self.avPlayer?.pause()
    }
    
    func startPlayback(){
        self.avPlayer?.play()
    }
    
    // A notification is fired and seeker is sent to the beginning to loop the video again
    @objc func playerItemDidReachEnd(notification: Notification) {
        let p: AVPlayerItem = notification.object as! AVPlayerItem
        p.seek(to: kCMTimeZero)
    }
}
