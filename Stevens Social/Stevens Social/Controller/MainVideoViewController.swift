//
//  MainVideoViewController.swift
//  Stevens Social
//
//  Created by Michael Kim, Vincent Porta on 3/26/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import CoreData
import Firebase
import FirebaseAuth
import Alamofire
import SwiftyJSON
import AVKit
import AVFoundation

class MainVideoViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UITabBarDelegate {

    @IBOutlet var videoView: UITableView!
    @IBOutlet var searchBox: UITextField!
    
    var videoArray:[Video] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()

        videoView.delegate = self
        videoView.dataSource = self
        
        configureTableView()
        
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        tableView.separatorStyle = .none
        let cell = tableView.dequeueReusableCell(withIdentifier: "videoTableCell", for: indexPath) as! VideoTableViewCell
        cell.selectionStyle = .none
        print(self.videoArray)
        let video = videoArray[indexPath.row]
        let videoURL = NSURL(string: video.src as! String)
        cell.videoTitle.text = video.title
        cell.videoPoster.text = "Vincent Porta"
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return videoArray.count
    }
    
    func playExternalVideo(videoURL: NSURL) {
        let player = AVPlayer(url: videoURL as URL)
        let playerViewController = AVPlayerViewController()
        playerViewController.player = player
        
        self.present(playerViewController, animated: true) { () -> Void in
            
            playerViewController.player!.play()
            
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func PlayVideoBtn(_ sender: Any) {
        performSegue(withIdentifier: "watchVideo", sender: self)
    }
    
    func getTitle(title: String) {
        let params: Parameters = ["name": title]
        Alamofire.request("http://localhost:5000/videos", parameters: params).responseJSON { response in

            if (response.result.error != nil) {
                print(response.result.error!)
            }
            
            if let value = response.result.value {
                let json = JSON(value)
                self.videoArray.removeAll() // This clears the array of previous search results (objects)
                for (_, subJson) in json["result"] {
                    print(subJson)
                    let id: String = subJson["_id"].stringValue
                    let title: String = subJson["title"].stringValue
                    let src: String = subJson["src"].stringValue
                    
                    self.videoArray.append(Video(_id: id, title: title, src: src))
                
                }
                DispatchQueue.main.async {
                    self.videoView.reloadData()
                }
                print(self.videoArray)
            }
        }
    }
    
    @IBAction func searchVideoButton(_ sender: UIButton) {
        print("button works")
        if searchBox.text != "" {
            let title = searchBox.text?.replacingOccurrences(of: " ", with: "")
            getTitle(title: title!)

        }
    }
    
    
    func configureTableView() {
        videoView.register(UINib(nibName: "VideoTableViewCell", bundle: nil), forCellReuseIdentifier: "videoTableCell")
        videoView.rowHeight = UITableViewAutomaticDimension
        videoView.estimatedRowHeight = 300.0
        
    }
}

