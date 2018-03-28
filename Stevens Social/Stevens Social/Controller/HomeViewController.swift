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


class HomeViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UITabBarDelegate {

    @IBOutlet var postTableView: UITableView!
    
    @IBOutlet var userEmail: UILabel!
    
    //Has attribute of postBody
    var postArray:[Post] = []
    
    let context = (UIApplication.shared.delegate as! AppDelegate).persistentContainer.viewContext
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do aUITableView setup after loading the view.
        
        postTableView.delegate = self
        postTableView.dataSource = self
        
        //fetch data from postArray
        self.fetchData()
        self.postTableView.reloadData()
        
//        print(FileManager.default.urls(for: .documentDirectory, in: .userDomainMask))
        configureTableView()
        configureEmail()

    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return postArray.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "postTableCell", for: indexPath)
        cell.selectionStyle = .none
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

    // fetch data from get api
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














