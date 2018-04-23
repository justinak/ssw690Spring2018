//
//  SearchDisplayUserViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta on 4/12/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import CoreData
import Firebase
import FirebaseAuth
import Alamofire
import SwiftyJSON


class SearchDisplayUserViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
    
    var userArray:[User] = []
    var uName: String = ""
    var uPhoto: UIImage?
    
    @IBOutlet var searchUsersTextBox: UITextField!
    
    @IBOutlet var searchUsersTableView: UITableView!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        searchUsersTableView.delegate = self
        searchUsersTableView.dataSource = self
        
        self.searchUsersTableView.reloadData()
        configureTableView()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
   
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return userArray.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "userResultCell", for: indexPath) as! UserResultTableViewCell
        cell.selectionStyle = .none
        cell.backgroundColor = UIColor.lightGray
        let user = userArray[indexPath.row]
        cell.userSearchDisplayName!.text = user.username
        let imgData = NSData(contentsOf: user.photo!)
        cell.userSearchImage.contentMode = .scaleAspectFit
        cell.userSearchImage.image = UIImage(data: imgData! as Data)
//        let imageUrl:URL = URL(string: self.userPhoto!)!
//        let imageData:NSData = NSData(contentsOf: imageUrl)!
//        let image = UIImage(data: imageData as Data)
        return cell
        
    }
    
    // method to run when table view cell is tapped
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        
        let user = tableView.cellForRow(at: indexPath) as! UserResultTableViewCell
        
        print(user.userSearchDisplayName.text!)
        
        uName = user.userSearchDisplayName.text!
        uPhoto = user.userSearchImage.image!
        
        // Segue to the profile view controller
        self.performSegue(withIdentifier: "sendToProfileView", sender: self)
    }
    
    // This function is called before the segue
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        
        let nav = segue.destination as! UINavigationController
        let svc = nav.topViewController as! ProfileViewController
        
        // set a variable in the profile view controller with the data to pass
        svc.data = uName
        svc.userPhoto = uPhoto
    }
    
    
    func getUser(name: String) {
        let params: Parameters = ["username": name]
        Alamofire.request("http://localhost:5000/api/users", parameters: params).responseJSON { response in
            
            if (response.result.error != nil) {
                print(response.result.error!)
            }
            
            if let value = response.result.value {
                let json = JSON(value)
                self.userArray.removeAll() // This clears the array of previous search results (objects)
                for (_, subJson) in json["result"] {
                    print(subJson)
                    let id: String = subJson["_id"].stringValue
                    let username: String = subJson["username"].stringValue
                    let photo: URL = subJson["photo"].url!
//                    let uuid: String = subJson["uuid"].stringValue
                    let followers: Array = subJson["follower"].array!
                    
                    self.userArray.append(User(_id: id, username: username, photo: photo, uuid: nil, followers: followers))
                    
                }
                DispatchQueue.main.async {
                    self.searchUsersTableView.reloadData()
                }
                print(self.userArray)
            }
        }
    }
    
    @IBAction func cancelUserSearch(_ sender: UIButton) {
        self.dismiss(animated: true, completion: nil)
    }
    
    @IBAction func searchUsersBtn(_ sender: UIButton) {
        print("search users working")
        if searchUsersTextBox.text != "" {
            let name = searchUsersTextBox.text?.replacingOccurrences(of: " ", with: "")
            getUser(name: name!)
            
        }
    }
    
    func configureTableView() {
        searchUsersTableView.register(UINib(nibName: "UserResultTableViewCell", bundle: nil), forCellReuseIdentifier: "userResultCell")
        searchUsersTableView.rowHeight = UITableViewAutomaticDimension
        searchUsersTableView.estimatedRowHeight = 190.0
        
    }

}
