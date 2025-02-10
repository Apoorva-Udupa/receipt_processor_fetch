import unittest
from receipt_processor.app import valid_receipt, calc_points

class TestValidReceipt(unittest.TestCase):
    """
    Tests for the valid_receipt() function

    1. missing_fields_test to test receipts with missing field
    2. no_items_test to test receipts when no items are present in receipt
    """

    def test_missing_fields(self):
        """
        A required field 'purchaseDate' is missing, hence it should return an error message.
        """
        data = {
            "retailer": "Target",
            "purchaseTime": "10:00",
            "items": [{"shortDescription": "Gummies", "price": "1.00"}],
            "total": "1.00"
        }
        err = valid_receipt(data)
        self.assertTrue(
            err and err.startswith("Missing required field:"),
            f"Expected a 'Missing required field:' error, got: {err}"
        )

    def test_no_items(self):
        """
        An empty item list cannot be in receipt atleast one item has to in the receipt, 
        it should return an error message.
        """
        data = {
            "retailer": "Target",
            "purchaseDate": "2022-10-10",
            "purchaseTime": "10:00",
            "items": [],
            "total": "1.00"
        }
        err = valid_receipt(data)
        self.assertEqual(
            err,
            "Receipt must have at least one item.",
            f"Expected 'Receipt must have at least one item.', got: {err}"
        )

    def test_valid_receipt(self):
        """
        All required fields exist => Should return None.
        """
        data = {
            "retailer": "Target",
            "purchaseDate": "2022-10-10",
            "purchaseTime": "10:00",
            "items": [{"shortDescription": "Widget", "price": "1.00"}],
            "total": "1.00"
        }
        err = valid_receipt(data)
        self.assertIsNone(
            err,
            f"Expected None for a valid receipt with all the fields, got error: {err}"
        )

class TestCalcPoints(unittest.TestCase):
    """
    1. test_rule1_alphanumeric - points for every alphanumeric character in retailer name.
    2. test_rule2_dollar_round - 50 points if the total is a round dollar amount with no cents.
    3. test_rule3_multiple25 - 25 points if the total is a multiple of 0.25.
    4. test_rule4_pairs_items - 5 points for every two items on the receipt.
    5. test_rule5_desc_length: If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned. 
    7. test_rule7_odd_day - 6 points if the day in the purchase date is odd.
    8. test_rule8_time_restiction - 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    """

    def test_rule1_alphanumeric(self):
        """
        Rule 1: points for every alphanumeric character in retailer name. 
        Here, we are checking for retailer - GAP (3 alphanumeric letters) hence it should return 3.
        No other rules are triggered.
        """
        receipt = {
            "retailer": "GAP",         
            "purchaseDate": "2022-10-10",  
            "purchaseTime": "09:00",       
            "total": "1.23",              
            "items": [
                {"shortDescription": "Tie-dye", "price": "1.23"}  
            ]
        }
        pts = calc_points(receipt)
        self.assertEqual(pts, 3, f"Expected 3 points from retailer 'GAP', got {pts}.")

    def test_rule2_dollar_round(self):
        """
         Rule 2: 50 points if the total is a round dollar amount with no cents.
         Here for 5.00 is a round dollar and .00 is multiple of 0.25 which is next rule hence (50+25points) total 75 points.
         
        """
        receipt = {
            "retailer": "",  
            "purchaseDate": "2022-10-10", 
            "purchaseTime": "09:00",      
            "total": "5.00",             
            "items": [
                {"shortDescription": "mini-toy", "price": "5.00"} 
            ]
        }
        pts = calc_points(receipt)
        self.assertEqual(pts, 75, f"Expected 75 points (50 for round +25 for .25 multiple - next rule), got {pts}.")


    def test_rule3_multiple25(self):
        """
        Rule 3: 25 points if the total is a multiple of 0.25.
        No other rules are triggered.
        """
        receipt = {
            "retailer": "",        
            "purchaseDate": "2022-10-10", 
            "purchaseTime": "09:00",     
            "total": "2.50",             
            "items": [
                {"shortDescription": "mini-toy", "price": "5.00"} 
            ]
        }
      
        pts = calc_points(receipt)
        self.assertEqual(pts, 25, f"Expected 25 for multiple of .25, got {pts}.")


    def test_rule4_pairs_items(self):
        """
        Rule 4: 5 points for every two items on the receipt.
        No other rules are triggered.
        """
        receipt = {
            "retailer": "", 
            "purchaseDate": "2022-10-10", 
            "purchaseTime": "09:00",
            "total": "5.10",   
            "items": [
                {"shortDescription": "ItemA", "price": "1.00"},  
                {"shortDescription": "ItemB", "price": "4.10"}   
            ]
        }
        pts = calc_points(receipt)
        self.assertEqual(pts, 5, f"Expected 5 points for every 2 items, got {pts}.")

    def test_rule5_desc_length(self):
        """
        Rule 5: If the trimmed length of the item description is a multiple of 3, 
        multiply the price by 0.2 and round up to the nearest integer. 
        No other rules are triggered.
        """
        receipt = {
            "retailer": "",            
            "purchaseDate": "2022-10-10", 
            "purchaseTime": "09:00",      
            "total": "2.01",            
            "items": [
                {"shortDescription": "Tie", "price": "2.01"} # length=3 => +ceil(2.01*0.2)=1
            ]
        }
        pts = calc_points(receipt)
        self.assertEqual(pts, 1, f"Expected 1 point for item desc multiple-of-3 only, got {pts}.")
    
    #NO RULE 6

    def test_rule7_odd_day(self):
        """
        Rule 7: 6 points if the day in the purchase date is odd.
        No other rules are triggered.
        """
        
        receipt = {
            "retailer": "",        
            "purchaseDate": "2022-05-05",#odd day
            "purchaseTime": "09:00",      
            "total": "1.10",             
            "items": [
                {"shortDescription": "ItemA", "price": "1.10"}  
            ]
        }
        pts = calc_points(receipt)
        self.assertEqual(pts, 6, f"Expected 6 points for odd day, got {pts}.")

    def test_rule8_time_restiction(self):
        """
        Rule 8: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        No other rules are triggered.
        """
        receipt = {
            "retailer": "",
            "purchaseDate": "2022-10-10", 
            "purchaseTime": "14:00",    
            "total": "3.10",           
            "items": [
                {"shortDescription": "Ties", "price": "3.10"} 
            ]
        }
        pts = calc_points(receipt)
        self.assertEqual(pts, 10, f"Expected 10 points for time 14:00, got {pts}.")


if __name__ == "__main__":
    unittest.main()
