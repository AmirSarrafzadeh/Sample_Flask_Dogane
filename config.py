import json
import random
import smtplib
import logging
import configparser
from flask import Flask, request, render_template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def check_email(email, domains):
    try:
        while True:
            if email.find("@") != -1:
                domain = email.split("@")[1]
                if domain in domains:
                    return email
                    break
                else:
                    print("Please give an institutional email located in Rome")
            else:
                print("please provide a valid email address")
    except Exception as ex:
        print("There is an error {} in getting email".format(ex))


def get_body(number):
    return '''<div style="margin:auto;max-width:600px;padding-top:50px" class="m_-2954602259193368226email-container">
    
    
    
    <table role="presentation" cellspacing="0" cellpadding="0" width="100%" align="center" id="m_-2954602259193368226logoContainer" style="background:#252f3d;border-radius:3px 3px 0 0;max-width:600px">
        <tbody><tr>
            <td style="background:#000000;border-radius:3px 3px 0 0;padding:20px 0 10px 0;text-align:center">
                <img src="https://media.discordapp.net/attachments/1105078065152929863/1105514855030599710/official3.jpg?width=671&height=671" width="75" height="75" alt="AWS logo" border="0" style="font-family:sans-serif;font-size:15px;line-height:140%;color:#555555" class="CToWUd" data-bit="iit">
            </td>
        </tr>
    </tbody></table>
    
    
    <table role="presentation" cellspacing="0" cellpadding="0" width="100%" align="center" id="m_-2954602259193368226emailBodyContainer" style="border:0px;border-bottom:1px solid #d6d6d6;max-width:600px">
        <tbody><tr>
            <td style="background-color:#fff;color:#444;font-family:'Amazon Ember','Helvetica Neue',Roboto,Arial,sans-serif;font-size:14px;line-height:140%;padding:25px 35px">
                <h1 style="font-size:20px;font-weight:bold;line-height:1.3;margin:0 0 15px 0">Verify your email address</h1>
                <p style="margin:0;padding:0">Thanks for starting the UniFit application. We want to make sure it's really a student of Rome. Please enter the following verification code when prompted. If you don’t want to enter to the app, you can ignore this message.</p>
                <p style="margin:0;padding:0"></p>
            </td>
        </tr>
        <tr>
            <td style="background-color:#fff;color:#444;font-family:'Amazon Ember','Helvetica Neue',Roboto,Arial,sans-serif;font-size:14px;line-height:140%;padding:25px 35px;padding-top:0;text-align:center">
                <div style="font-weight:bold;padding-bottom:15px">Verification code</div>
                <div style="color:#000;font-size:36px;font-weight:bold;padding-bottom:15px">''' + number + '''</div>
                <div>(This code is valid for 10 minutes)</div>
            </td>
        </tr>
        <tr>
            <td style="background-color:#fff;border-top:1px solid #e0e0e0;color:#777;font-family:'Amazon Ember','Helvetica Neue',Roboto,Arial,sans-serif;font-size:14px;line-height:140%;padding:25px 35px">
                <p style="margin:0 0 15px 0;padding:0 0 0 0">UniFit Application will never email you and ask you to disclose or verify your password, credit card, or banking account number.</p>
            </td>
        </tr>
    </tbody></table>
    
    
    <table role="presentation" cellspacing="0" cellpadding="0" width="100%" align="center" id="m_-2954602259193368226footer" style="max-width:600px">
        <tbody><tr>
            <td style="color:#777;font-family:'Amazon Ember','Helvetica Neue',Roboto,Arial,sans-serif;font-size:12px;line-height:16px;padding:20px 30px;text-align:center">
                This message was produced and distributed by UniFit application, Inc., Via Giacomo Peroni, 400, Rome, Inc.. All rights reserved. UniFit is a registered trademark of <a href="https://bjdxkhre.r.us-east-1.awstrack.me/L0/https:%2F%2Fwww.wheretech.it%2F/1/01000187e66aa252-c17220a5-86e1-4dc6-ad4b-f81b5d0b8cec-000000/03QNw982mt3YJb3QFHMXcG7kAEo=320" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://bjdxkhre.r.us-east-1.awstrack.me/L0/https:%252F%252Fwww.wheretech.it%252F/1/01000187e66aa252-c17220a5-86e1-4dc6-ad4b-f81b5d0b8cec-000000/03QNw982mt3YJb3QFHMXcG7kAEo%3D320&amp;source=gmail&amp;ust=1683814418406000&amp;usg=AOvVaw2EqApahIaC2Z5Iz-ID3POb">wheretech,it</a>, Inc. View our <a href="https://bjdxkhre.r.us-east-1.awstrack.me/L0/https:%2F%2Fwww.wheretech,it%2Fgp%2Ff.html%3FC=ASNZCWDUG167%26M=urn:rtn:msg:20201117075724eb4b304704de4791b90718772250p0na%26R=24F5VU3RW0OAG%26T=C%26U=https%253A%252F%252Faws.wheretech,it%252Fprivacy%252F%253Fsc_channel%253Dem%2526sc_campaign%253Dwlcm%2526sc_publisher%253Daws%2526sc_medium%253Dem_wlcm_footer%2526sc_detail%253Dwlcm_footer%2526sc_content%253Dother%2526sc_country%253Dglobal%2526sc_geo%253Dglobal%2526sc_category%253Dmult%2526ref_%253Dpe_1679150_261538020%26H=PSTTW2QUTETQPANYMBJB5CSZMMSA%26ref_=pe_1679150_261538020/1/01000187e66aa252-c17220a5-86e1-4dc6-ad4b-f81b5d0b8cec-000000/VSUKcWE4mXtuWBhdIbjK6DTRbvs=320" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://bjdxkhre.r.us-east-1.awstrack.me/L0/https:%252F%252Fwww.wheretech,it%252Fgp%252Ff.html%253FC%3DASNZCWDUG167%2526M%3Durn:rtn:msg:20201117075724eb4b304704de4791b90718772250p0na%2526R%3D24F5VU3RW0OAG%2526T%3DC%2526U%3Dhttps%25253A%25252F%25252Faws.wheretech,it%25252Fprivacy%25252F%25253Fsc_channel%25253Dem%252526sc_campaign%25253Dwlcm%252526sc_publisher%25253Daws%252526sc_medium%25253Dem_wlcm_footer%252526sc_detail%25253Dwlcm_footer%252526sc_content%25253Dother%252526sc_country%25253Dglobal%252526sc_geo%25253Dglobal%252526sc_category%25253Dmult%252526ref_%25253Dpe_1679150_261538020%2526H%3DPSTTW2QUTETQPANYMBJB5CSZMMSA%2526ref_%3Dpe_1679150_261538020/1/01000187e66aa252-c17220a5-86e1-4dc6-ad4b-f81b5d0b8cec-000000/VSUKcWE4mXtuWBhdIbjK6DTRbvs%3D320&amp;source=gmail&amp;ust=1683814418406000&amp;usg=AOvVaw1eLoGAqcfkzLZWJylk6e-L">privacy policy</a>.
            </td>
        </tr>
    </tbody></table>
    
    
</div>'''


