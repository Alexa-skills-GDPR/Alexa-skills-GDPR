# Understanding GDPR Non-Compliance in Privacy Policies of Alexa Skills in European Marketplaces

## Abstract

Amazon Alexa is one of the largest Voice Personal Assistant (VPA) platforms and it allows third-party developers to publish their voice apps, named skills, to the Alexa skill store. To satisfy the needs of European users, Amazon Alexa established multiple skill marketplaces in Europe and allows developers to publish skills in their native languages, such as German, French, Italian, and Spanish. Skills targeting users in European countries are required to comply with GDPR (General Data Protection Regulation), which imposes strict obligations on data collection and processing. Skills that involve data collection should provide a privacy policy to disclose the data practice to users and meet GDPR requirements. 

In this work, we analyze privacy policies of skills in European marketplaces, focusing on whether skills’ privacy policies and data collection behaviors comply with GDPR. We collect a large-scale European skill dataset that includes skills in all European marketplaces with privacy policies. To classify whether a sentence in a privacy policy provides GDPR information, we gather a labeled dataset consisting of skills’ privacy policy sentences and train a BERT model for classification. Then we analyze the GDPR compliance of European skills. Using a dynamic testing tool based on ChatGPT, we check whether skills’ privacy policies comply with GDPR and are consistent with the actual data collection behaviors. Surprisingly, we find that 67% of privacy policies fail to comply  with GDPR and don’t provide necessary GDPR-related information. For 1,187 skills with data collection behaviors, we find that 603 skills (50.8%) don’t provide a complete privacy policy and 1,128 skills (95%) have GDPR non-compliance issues in their privacy policies. Meanwhile, we find that the GDPR has a positive influence on European privacy policies when compared to non-European marketplaces, such as the United States, Mexico and Brazil.

Category | Article | Label
--- | --- | --- 
1 |13.1 | Collect Personal Information
2 |13.2(a) |Data Retention Period
3 |13.1(c) |Data Processing Purposes
4 |13.1(a)(b) |Contact Details
5 |13.2(b) |Right to Access
6 |13.2(b) |Right to Rectify or Erase
7 |13.2(b)  |Right to Restrict of Processing
8 |13.2(b)  |Right to Object to Processing
9 |13.2(b)  |Right to Data Portability
10 |13.2(d)  |Right to Lodge a Complaint

![overall](https://github.com/Alexa-skills-GDPR/Alexa-skills-GDPR/blob/main/image/gdpr.png)
<img src="https://github.com/Alexa-skills-GDPR/Alexa-skills-GDPR/blob/main/image/conversation.png" width="400">
<img src="https://github.com/Alexa-skills-GDPR/Alexa-skills-GDPR/blob/main/image/permission.png" width="412">
