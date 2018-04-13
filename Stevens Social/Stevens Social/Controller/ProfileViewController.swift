//
//  ProfileViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta on 4/13/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import Firebase
import FirebaseAuth
import Alamofire
import SwiftyJSON

class ProfileViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {

    @IBOutlet var nameHere: UILabel!
    @IBOutlet var profileViewImage: UIImageView!
    @IBOutlet var bioProfileView: UILabel!
    @IBOutlet var numOfFollowers: UILabel!
    @IBOutlet var numOfFollowing: UILabel!
    @IBOutlet var profileViewTableView: UITableView!
    @IBOutlet var followBtnText: UIButton!
    
    var data = ""
    var userPhoto: UIImage?
    var postsArray:[Post] = []
    var isFollowing: Bool = false
    
    override func viewDidLoad() {
        super.viewDidLoad()
    
        nameHere.text = data
        profileViewImage.image = userPhoto
        profileViewTableView.delegate = self
        profileViewTableView.dataSource = self
        
        self.fetchData()
        self.profileViewTableView.reloadData()
        
        configureTableView()
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }

    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return postsArray.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "postTableCell", for: indexPath) as! PostTableViewCell
        cell.selectionStyle = .none
        
        let post = postsArray[indexPath.row]
        cell.postBody!.text = post.text
        cell.postName!.text = post.created_by
//        cell.postBody!.alpha = 0
//        cell.postName!.alpha = 0
//        UIView.animate(withDuration: 0.5, animations: {
//            cell.postBody!.alpha = 1
//            cell.postName!.alpha = 1
//        })
        
        
        //        let imageUrl:URL = URL(string: self.userPhoto!)!
        //        let imageData:NSData = NSData(contentsOf: imageUrl)!
        //        let image = UIImage(data: imageData as Data)
        //        cell.avatarImageView!.image = image
        //        cell.avatarImageView.contentMode = UIViewContentMode.scaleAspectFit
        
        return cell
    }
    
    func configureTableView() {
        profileViewTableView.register(UINib(nibName: "PostTableViewCell", bundle: nil), forCellReuseIdentifier: "postTableCell")
        profileViewTableView.rowHeight = UITableViewAutomaticDimension
        profileViewTableView.estimatedRowHeight = 350.0
        
    }
    
    func fetchData(){
        // Search for posts based on created_by field
        let params: Parameters = ["created_by": self.data] //
        Alamofire.request("http://localhost:5000/api/posts/get-username", parameters: params).responseJSON { response in
            
            if (response.result.error != nil) {
                print(response.result.error!)
            }
            
            if let value = response.result.value {
                let json = JSON(value)
                for (_, subJson) in json["result"] {
                    print(subJson)
                    let id: String = subJson["_id"].stringValue
                    let text: String = subJson["text"].stringValue
                    let uid: String = subJson["uuid"].stringValue
                    let likes: Array<Any> = []
                    let created_by: String = subJson["created_by"].stringValue
                    
                    self.postsArray.append(Post(_id: id, text: text, image: nil, uuid: uid, likes: likes, created_by: created_by))
                    
                    
                }
                
                DispatchQueue.main.async {
                    self.profileViewTableView.reloadData()
                }
                print(self.postsArray.reverse())
            }
        }
        
    }
    
    @IBAction func profileViewFollowBtn(_ sender: UIButton) {
        print("follow button pressed")
        if isFollowing == false {
            followBtnText.setTitle("Following", for: UIControlState.normal)
            isFollowing = true
        } else if isFollowing == true {
            followBtnText.setTitle("Follow", for: UIControlState.normal)
            isFollowing = false
        }
    }
    
}
