//
//  AppDelegate.swift
//  Stevens Social
//
//  Created by Vincent Porta, Michael Kim on 2/28/18.
//  Copyright © 2018 Stevens. All rights reserved.
//

import UIKit
import AWSMobileClient
import CoreData
import Firebase

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?


    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplicationLaunchOptionsKey: Any]?) -> Bool {
        
        FirebaseApp.configure()
        return true
//        return AWSMobileClient.sharedInstance().interceptApplication(
//            application,
//            didFinishLaunchingWithOptions: launchOptions)
    }

    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
        // Saves changes in the application's managed object context before the application terminates.

    }
    
    

}

