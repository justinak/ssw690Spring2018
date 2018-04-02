//
//  VideoTableViewCell.swift
//  Stevens Social
//
//  Created by Vincent Porta on 3/31/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit

class VideoTableViewCell: UITableViewCell {

    @IBOutlet var videoThumbnail: UIImageView!
    @IBOutlet var videoTitle: UILabel!
    @IBOutlet var videoPoster: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
}
