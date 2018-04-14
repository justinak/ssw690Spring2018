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
    var uid: String?
    var uName: String?
    var uPhoto: UIImage?
    
    var userName: String?
    var userImage: UIImage?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        Auth.auth().addStateDidChangeListener { (auth, user) in
            self.uid = user?.uid
        }   
        postTableView.delegate = self
        postTableView.dataSource = self
        
        //fetch data from postArray
        //self.fetchData()
        self.postTableView.reloadData()
        //self.runGetRequestForUserPhoto()
        self.configureTableView()
        self.configureEmail()

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
        cell.quackCount!.text = "\(quackCount)"
        cell.avatarImageView.contentMode = UIViewContentMode.scaleAspectFit
        cell.avatarImageView!.image = uPhoto
        cell.postBody!.alpha = 0
        cell.postName!.alpha = 0
        cell.quackCount!.alpha = 0
        cell.avatarImageView!.alpha = 0
        UIView.animate(withDuration: 0.5, animations: {
            cell.postBody!.alpha = 1
            cell.postName!.alpha = 1
            cell.quackCount!.alpha = 1
            cell.avatarImageView!.alpha = 1
        })
        
        return cell
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    // fetch data from get api
    func fetchData(){
        
        let params: Parameters = ["uuid": self.uid!] // replace string with Firebase uid!
        Alamofire.request("http://localhost:5000/api/get/timeline", parameters: params).responseJSON { response in
            
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
                    
                    self.postsArray.append(Post(_id: id, text: text, image: nil, uuid: uid, likes: likes, created_by: created_by))
                    
                    // Must change 000002 to Firebase uid!
                    if (subJson["uuid"].stringValue == self.uid!) {
                        self.uName = created_by
                    }
                    
                }
                DispatchQueue.main.async {
                    self.postTableView.reloadData()
                    self.userEmail.text = self.uName
                }
                print(self.postsArray)
            }
        }
    }
    
    func runGetRequestForUserPhoto() {
        let params: Parameters = ["uuid": self.uid!] // replace string with Firebase uid!
        Alamofire.request("http://localhost:5000/api/user/getone", parameters: params).responseJSON { response in
            
            if (response.result.error != nil) {
                print(response.result.error!)
            }
            
            if let value = response.result.value {
                let json = JSON(value)
                var photo: String?
                for (_, subJson) in json["result"] {
                    print(subJson)
                    photo = subJson["photo"].stringValue
                }
                
                DispatchQueue.main.async {
                    self.postTableView.reloadData()
                    let imageUrl:URL = URL(string: photo!)!
                    let imageData:NSData = NSData(contentsOf: imageUrl)!
                    let image = UIImage(data: imageData as Data)
                    self.uPhoto = image
                }
            }
        }
    }
    
    @IBAction func logOutPressed(_ sender: Any) {
        do {
            try Auth.auth().signOut()
            navigationController?.popToRootViewController(animated: true)
            print("signout successful")
        }
        catch {
            print("Error: there was a problem logging out")
        }
    }
    
    func configureTableView() {
        postTableView.register(UINib(nibName: "PostTableViewCell", bundle: nil), forCellReuseIdentifier: "postTableCell")
        postTableView.rowHeight = UITableViewAutomaticDimension
        postTableView.estimatedRowHeight = 350.0
        
    }
    
    func configureEmail() {
        Auth.auth().addStateDidChangeListener { (auth, user) in
            self.userEmail.text = user?.email
        }
    }

}














