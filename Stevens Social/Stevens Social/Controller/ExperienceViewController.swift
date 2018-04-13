//
//  ExperienceViewController.swift
//  Stevens Social
//
//  Created by Michael Kim on 4/10/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON

class ExperienceViewController: UIViewController, UICollectionViewDataSource, UICollectionViewDelegate {
    
    @IBOutlet weak var expColl: UICollectionView!
    var ExperiencePosts:[Experiences] = []

    @IBAction func likeButton(_ sender: Any) {
     
        
    }
    @IBAction func dislikeButton(_ sender: Any) {
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    
        Alamofire.request("http://127.0.0.1:5000/api/get/experiences").responseJSON { response in
            //print("Request: \(String(describing: response.request))")   // original url request
            //print("Response: \(String(describing: response.response))") // http url response
            //print("Result: \(response.result)")
        // response serialization result
        
            if (response.result.error != nil) {
                print(response.result.error!)
            }
                if let value = response.result.value{
                let json = JSON(value)
                for (_, subJson) in json["result"] {
                    print("subJson: ",subJson)
                    let experience = subJson["experience"].stringValue
                    let _id = subJson["_id"].stringValue
                    let time = subJson["time"].stringValue
                    let userid = subJson["userid"].stringValue
                    let votes = subJson["votes"].stringValue
                    self.ExperiencePosts.append(Experiences(experience: experience, _id: _id, time: time, userid: userid, votes: votes))
                }
    
                    DispatchQueue.main.async {
                    print("DATA: \(self.ExperiencePosts)")
                    self.expColl.reloadData()
                }
            }
        }
        self.expColl.reloadData()
    }
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return self.ExperiencePosts.count
    }
    
    func numberOfSections(in collectionView: UICollectionView) -> Int {
        return 1
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "experienceCell", for: indexPath) as! ExperienceCollectionViewCell
        
        let experience = self.ExperiencePosts[indexPath.row]
        
        cell.experiencePost.text = experience.experience
        cell.timePost.text = experience.time
        cell.votePost.text = experience.votes

        cell.contentView.layer.cornerRadius = 7.0
        cell.contentView.layer.borderWidth = 1.0
        cell.contentView.layer.borderColor = UIColor.clear.cgColor
        cell.contentView.layer.masksToBounds = false
        cell.layer.shadowColor = UIColor.gray.cgColor
        cell.layer.shadowOffset = CGSize(width: 0, height: 1.0)
        cell.layer.shadowOpacity = 1.0
        cell.layer.masksToBounds = false
        cell.layer.shadowRadius = 7.0
        cell.layer.shadowPath = UIBezierPath(roundedRect: cell.bounds, cornerRadius: cell.contentView.layer.cornerRadius).cgPath

        return cell
    }
}

