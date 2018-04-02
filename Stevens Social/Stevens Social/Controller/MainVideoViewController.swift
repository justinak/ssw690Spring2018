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

class MainVideoViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UITabBarDelegate {

    @IBOutlet var videoView: UITableView!
    @IBOutlet var searchBox: UITextField!
    
    var videoArray:[Video] = []

    override func viewDidLoad() {
        super.viewDidLoad()

        videoView.delegate = self
        videoView.dataSource = self

        self.videoView.reloadData()
        configureTableView()
        
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "videoTableCell", for: indexPath) as! VideoTableViewCell
        cell.selectionStyle = .none
//        let video = videoArray[indexPath.row]
        let messageArray = ["one", "two", "three"]
        cell.videoTitle.text = messageArray[indexPath.row]
//        cell.videoTitle.text = video.title
//        cell.videoPoster.text = video.src

        return cell
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 3
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

            if let value = response.result.value {
                let json = JSON(value)
                for (_, subJson) in json["result"] {
                    print(subJson)
                    let id: String = subJson["_id"].stringValue
                    let title: String = subJson["title"].stringValue
                    let src: String = subJson["src"].stringValue

                self.videoArray.append(Video(_id: id, title: title, src: src))
                
                }
//                print(self.videoArray)
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
        videoView.estimatedRowHeight = 350.0
        
    }
}
