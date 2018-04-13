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
    }
 
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
    }
}
