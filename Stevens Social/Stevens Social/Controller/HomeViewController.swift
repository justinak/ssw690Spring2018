//
//  HomeViewController.swift
//  Stevens Social
//
//  Created by Vincent Porta on 3/5/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit

class HomeViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UITabBarDelegate {
    
    
    @IBOutlet var postTableView: UITableView!
    
//    @IBOutlet var homeTab: UITabBarItem!
//    @IBOutlet var interviewTab: UITabBarItem!
//    @IBOutlet var videosTab: UITabBarItem!
//    @IBOutlet var profileTab: UITabBarItem!
    
//    @IBOutlet var tabBar: UITabBar!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do aUITableView setup after loading the view.
        
        postTableView.delegate = self
        postTableView.dataSource = self
        
        postTableView.register(UINib(nibName: "PostTableViewCell", bundle: nil), forCellReuseIdentifier: "postTableCell")
        configureTableView()
    
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func logOutButton(_ sender: UIButton) {
        
//        performSegue(withIdentifier: "", sender: <#T##Any?#>)
    }
    
    //  This method gets called for every cell in the post table view cell
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let cell = tableView.dequeueReusableCell(withIdentifier: "postTableCell", for: indexPath) as! PostTableViewCell
        let postArray = ["I like pie.", "I don't like pie", "I've never eaten pie"]
        
        cell.postBody.text = postArray[indexPath.row]
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 3
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
