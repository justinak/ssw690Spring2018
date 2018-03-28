//
//  PostTableViewCell.swift
//  Stevens Social
//
//  Created by Vincent Porta on 3/5/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit

class PostTableViewCell: UITableViewCell {

    @IBOutlet var avatarImageView: UIImageView!
    @IBOutlet var postBody: UILabel!
    @IBOutlet var postName: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
    @IBAction func shareButton(_ sender: UIButton) {
        print("shareButton pressed")
    }
    
    @IBAction func quackButton(_ sender: UIButton) {
        print("quackButton pressed")

    }
    
}
