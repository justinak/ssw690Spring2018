//
//  UserResultTableViewCell.swift
//  Stevens Social
//
//  Created by Vincent Porta on 4/12/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit

class UserResultTableViewCell: UITableViewCell {

    @IBOutlet var userSearchImage: UIImageView!
    
    @IBOutlet var userSearchDisplayName: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
//        let gestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(self.labelTapped))
//        userSearchDisplayName.addGestureRecognizer(gestureRecognizer)
    }
 
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
    }
    
//    @objc func labelTapped() {
//        print("labelTapped tapped")
//        print(userSearchDisplayName.text!)
//
//    }
    
    

    
}
