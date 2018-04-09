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
    var aboutToBecomeInvisibleCell = -1
    var avPlayerLayer: AVPlayerLayer!
    var firstLoad = true
    var visibleIP : IndexPath?
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        videoView.delegate = self
        videoView.dataSource = self
        
        configureTableView()
        visibleIP = IndexPath.init(row: 0, section: 0)
       
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        tableView.separatorStyle = .none
        let cell = tableView.dequeueReusableCell(withIdentifier: "videoTableCell", for: indexPath) as! VideoTableViewCell
        cell.selectionStyle = .none
        let video = videoArray[indexPath.row]
        cell.videoTitle.text = video.title
        cell.videoPoster.text = "Vincent Porta" // Need a user email address to be displayed here. 
        cell.videoPlayerItem = AVPlayerItem.init(url: video.src! )

        return cell
    }
    
    func playVideoOnTheCell(cell : VideoTableViewCell, indexPath : IndexPath){
        cell.startPlayback()
    }
    
    func stopPlayBack(cell : VideoTableViewCell, indexPath : IndexPath){
        cell.stopPlayback()
    }
    
    func tableView(_ tableView: UITableView, didEndDisplaying cell: UITableViewCell, forRowAt indexPath: IndexPath) {
        print("end = \(indexPath)")
        if let videoCell = cell as? VideoTableViewCell {
            videoCell.stopPlayback()
        }
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return videoArray.count
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 290
    }
    
    func tableView(_ tableView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
        return 0
    }
    
    func scrollViewDidScroll(_ scrollView: UIScrollView) {
        let indexPaths = self.videoView.indexPathsForVisibleRows
        var cells = [Any]()
        for ip in indexPaths!{
            if let videoCell = self.videoView.cellForRow(at: ip) as? VideoTableViewCell{
                cells.append(videoCell)
            }
        }
        let cellCount = cells.count
        if cellCount == 0 {return}
        if cellCount == 1{
            if visibleIP != indexPaths?[0]{
                visibleIP = indexPaths?[0]
            }
            if let videoCell = cells.last! as? VideoTableViewCell{
                self.playVideoOnTheCell(cell: videoCell, indexPath: (indexPaths?.last)!)
            }
        }
        if cellCount >= 2 {
            for i in 0..<cellCount{
                let cellRect = self.videoView.rectForRow(at: (indexPaths?[i])!)
                let intersect = cellRect.intersection(self.videoView.bounds)
                //                currentHeight is the height of the cell that
                //                is visible
                let currentHeight = intersect.height
                print("\n \(currentHeight)")
                let cellHeight = (cells[i] as AnyObject).frame.size.height
                //                0.95 here denotes how much you want the cell to display
                //                for it to mark itself as visible,
                //                .95 denotes 95 percent,
                //                you can change the values accordingly
                if currentHeight > (cellHeight * 0.95){
                    if visibleIP != indexPaths?[i]{
                        visibleIP = indexPaths?[i]
                        print ("visible = \(indexPaths?[i])")
                        if let videoCell = cells[i] as? VideoTableViewCell{
                            self.playVideoOnTheCell(cell: videoCell, indexPath: (indexPaths?[i])!)
                        }
                    }
                }
                else{
                    if aboutToBecomeInvisibleCell != indexPaths?[i].row{
                        aboutToBecomeInvisibleCell = (indexPaths?[i].row)!
                        if let videoCell = cells[i] as? VideoTableViewCell{
                            self.stopPlayBack(cell: videoCell, indexPath: (indexPaths?[i])!)
                        }
                        
                    }
                }
            }
        }
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
                    let src: URL = subJson["src"].url!
                    let userID: String = subJson["user_id"].stringValue
                    
                    self.videoArray.append(Video(_id: id, title: title, src: src, user_id: nil))
            
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
        videoView.estimatedRowHeight = 290.0
        
    }
}

