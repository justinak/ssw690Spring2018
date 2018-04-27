//
//  HomeViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta on 3/5/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import CoreData
import Firebase
import FirebaseAuth
import Alamofire
import SwiftyJSON

class HomeViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UITabBarDelegate {

    @IBOutlet var postTableView: UITableView!
    @IBOutlet var userEmail: UILabel!
    
    var postsArray:[Post] = []
    var uName: String?
    
    var userName: String?
    var userImage: UIImage?

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        postsArray.removeAll()
        self.fetchData()
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        
        postTableView.delegate = self
        postTableView.dataSource = self
        self.fetchData()
        self.configureTableView()

        
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
        let quackCount = post.likes.count
        cell.postBody!.text = post.text
        cell.postName!.text = post.created_by
//        cell.quackCount!.text = "\(quackCount)"
        cell.avatarImageView.contentMode = UIViewContentMode.scaleAspectFit
        let imageUrl:URL = URL(string: post.image!)!
        let imageData:NSData = NSData(contentsOf: imageUrl)!
        let image = UIImage(data: imageData as Data)
        cell.avatarImageView!.image = image
        
        return cell
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
        postsArray.removeAll()
    }

    // fetch data from get api
    func fetchData() {
       var userPhoto: String?
        Auth.auth().addStateDidChangeListener { (auth, user) in
            if let user = user {
                self.userEmail.text = user.email

                let params: Parameters = ["uuid": (user.uid)]
                Alamofire.request("https://stevens-social-app.herokuapp.com/api/get/timeline", parameters: params).responseJSON { response in
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
                            let likes: Array<Any> = subJson["likes"].array!
                            let created_by: String = subJson["created_by"].stringValue
                            
                            // 2nd api call to get user photos
                            let param: Parameters = ["uuid": uid] // replace string with Firebase uid!
                            Alamofire.request("https://stevens-social-app.herokuapp.com/api/user/getone", parameters: param).responseJSON { response in
                                if (response.result.error != nil) {
                                    print(response.result.error!)
                                }
                                
                                if let value = response.result.value {
                                    let json2 = JSON(value)
                        
                                    userPhoto = json2["result"][0]["photo"].stringValue

                                    self.postsArray.append(Post(_id: id, text: text, image: userPhoto, uuid: uid, likes: likes, created_by: created_by))

                                } // end second if statement

                                DispatchQueue.main.async {
                                    self.postTableView.reloadData()
                                }
                            } // end second request
                            

                        } // end first for loop
                    
                    }
                } // end alamofire request
            }
        }
        print("###################")
        print(self.postsArray)
    }
    
    @IBAction func logOutPressed(_ sender: Any) {
        do {
            try Auth.auth().signOut()
            if let storyboard = self.storyboard {
                let vc = storyboard.instantiateViewController(withIdentifier: "firstVC") as! UINavigationController
                self.present(vc, animated: false, completion: nil)
            }
            print("signout successful")
        }
        catch let error {
            print("Error: there was a problem logging out: \(error)")
        }
    }
    
    func configureTableView() {
        postTableView.register(UINib(nibName: "PostTableViewCell", bundle: nil), forCellReuseIdentifier: "postTableCell")
        postTableView.rowHeight = UITableViewAutomaticDimension
        postTableView.estimatedRowHeight = 350.0
        
    }
}














