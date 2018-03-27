//
//  helper.swift
//  Stevens Social
//
//  Created by Vincent Porta on 3/27/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import Foundation

class API {
    
    var route: String = ""
    var method: String = ""
    
    init(customRoute : String, customMethod : String) {
        self.route = customRoute
        self.method = customMethod
    }
    
    func sendRequest(parameters: Dictionary<String, String>) {
        var ur = URL(string: route)!
        print(ur)
        let session = URLSession.shared
        var request = URLRequest(url: ur)
        request.httpMethod = method
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: .prettyPrinted) // pass dictionary to nsdata object and set it as request body
            
        } catch let error {
            print(error.localizedDescription)
        }
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue("application/json", forHTTPHeaderField: "Accept")
        
        let task = session.dataTask(with: request as URLRequest, completionHandler: { data, response, error in
            
            guard error == nil else {
                return
            }
            
            guard let data = data else {
                return
            }
            
            do {
                //create json object from data
                if let json = try JSONSerialization.jsonObject(with: data, options: .mutableContainers) as? [String: Any] {
                    print(json)
                    // handle json...
                }
                
            } catch let error {
                print(error.localizedDescription)
            }
        })
        task.resume()
    }
}
