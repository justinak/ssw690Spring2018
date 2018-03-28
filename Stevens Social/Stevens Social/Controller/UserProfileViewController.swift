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

class UserProfileViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UITabBarDelegate {
    
    @IBOutlet var postTableViewProfile: UITableView!
    var postArray:[Post] = []
    
    let context = (UIApplication.shared.delegate as! AppDelegate).persistentContainer.viewContext
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
        return postArray.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "postTableCell", for: indexPath)
        //first post data will be stored into post
        let post = postArray[indexPath.row]
        cell.textLabel!.text = post.postBody!
        //get from post
        //cell.postName!.text = post.email
        return cell
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func fetchData(){
        //fetch data from Post and put data in postArray
//        Alamofire.request("http://127.0.0.1:5000/api/posts/get").response { response in
//            print(response)
//            if let json = response.result.value {
//                print("JSON: \(json)") // serialized json response
//            }
//
//            if let data = response.data, let utf8Text = String(data: data, encoding: .utf8) {
//                print("Data: \(utf8Text)") // original server data as UTF8 string
//            }
//        }
        
        do {
            postArray = try context.fetch(Post.fetchRequest())
        } catch {
            print(error)
        }
        
    }
    
    func configureTableView() {
        postTableViewProfile.register(UINib(nibName: "PostTableViewCell", bundle: nil), forCellReuseIdentifier: "postTableCell")
        postTableViewProfile.rowHeight = UITableViewAutomaticDimension
        postTableViewProfile.estimatedRowHeight = 350.0
        
    }
    

}
