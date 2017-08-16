//
//  ViewControlerBuiltinTypes.swift
//  hello_swift
///
//  Copyright © 2017 HERE. All rights reserved.
//

import UIKit
import hello

class ViewControllerBuiltinTypes: UIViewController {
    @IBOutlet var textLoanAmount: UITextField!
    @IBOutlet var textInterestRate: UITextField!
    @IBOutlet var textResult: UILabel!

    @IBAction func didPressButton(_ sender: Any) {
        textLoanAmount.resignFirstResponder()
        textInterestRate.resignFirstResponder()
        guard
            let loanText = textLoanAmount.text,
            let loanAmount = Float(loanText)
        else {
            textResult.text = "Provide proper loan ammount!"
            return
        }
        guard
            let interestText = textInterestRate.text,
            let interestRate = Int8(interestText)
        else {
            textResult.text = "Provide proper interest rate!"
            return
        }

        let result = HelloWorldBuiltinTypes.methodWithFloatAndInteger(
            inputFloat: loanAmount, inputInteger: interestRate)
        textResult.text = String(result)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}
