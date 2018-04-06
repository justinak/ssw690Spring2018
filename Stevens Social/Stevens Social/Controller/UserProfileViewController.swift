//
//  UserProfileViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta on 3/2/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import CoreData
import Firebase
import FirebaseAuth
import Alamofire
import SwiftyJSON

class UserProfileViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UITabBarDelegate {
    
    @IBOutlet weak var followBtnText: UIButton!
    @IBOutlet var postTableViewProfile: UITableView!

    var postsArray:[Post] = []
    var isFollowing: Bool = false
    var uid: String?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        Auth.auth().addStateDidChangeListener { (auth, user) in
            self.uid = user?.uid
        }
        postTableViewProfile.delegate = self
        postTableViewProfile.dataSource = self
        
        //fetch data from postArray
        self.fetchData()
        self.postTableViewProfile.reloadData()
        
        configureTableView()
    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return postsArray.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "postTableCell", for: indexPath) as! PostTableViewCell
        //first post data will be stored into post
        let post = postsArray[indexPath.row]
        cell.postBody!.text = post.text
        cell.postName!.text = post.uuid as! String as! String
        
        return cell
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func fetchData(){
//        do {
//            postArray = try context.fetch(Post.fetchRequest())
//        } catch {
//            print(error)
//        }
        
        let params: Parameters = ["uuid": "000002"] // replace string with Firebase uid! 
        Alamofire.request("http://localhost:5000/api/posts/get", parameters: params).responseJSON { response in
            
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
                    
                    self.postsArray.append(Post(_id: id, text: text, image: nil, uuid: uid, likes: likes))
                    
                }
                DispatchQueue.main.async {
                    self.postTableViewProfile.reloadData()
                }
                print(self.postsArray)
            }
        }
        
    }
    
    func configureTableView() {
        postTableViewProfile.register(UINib(nibName: "PostTableViewCell", bundle: nil), forCellReuseIdentifier: "postTableCell")
        postTableViewProfile.rowHeight = UITableViewAutomaticDimension
        postTableViewProfile.estimatedRowHeight = 350.0
        
    }
    
    @IBAction func followBtn(_ sender: UIButton) {
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
