//
//  HomeViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta on 3/5/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import CoreData

class HomeViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UITabBarDelegate {

    @IBOutlet var postTableView: UITableView!
    
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
        
        print(FileManager.default.urls(for: .documentDirectory, in: .userDomainMask))
        
       // postTableView.register(UINib(nibName: "PostTableViewCell", bundle: nil), forCellReuseIdentifier: "postTableCell")
       // configureTableView()

    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return postArray.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "postcell", for: indexPath)
        //first post data will be stored into post
        let post = postArray[indexPath.row]
        cell.textLabel!.text = post.postBody!
        
        return cell
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func fetchData(){
        do{
            //fetch data from Post and put data in postArray
            postArray = try context.fetch(Post.fetchRequest())
        }catch{
            print(error)
        }
    }
    
    @IBAction func logOutPressed(_ sender: Any) {
        //        do {
        // Here we need to use an Auth() method to log out.
        //            try
        navigationController?.popToRootViewController(animated: true)
        
        //        }
        //        catch {
        //            print("error: there was a problem logging out")
        //        }
    }
    
    func configureTableView() {
        postTableView.rowHeight = UITableViewAutomaticDimension
        postTableView.estimatedRowHeight = 120.0
    }
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
