import json
import datetime 
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    playerDataBase = dynamodb.Table("playerDatabase")
    params = event['queryStringParameters']
    playerid = params['playerID']
    newSkill = params['skill']
    updatedPlayerRESP = playerDataBase.get_item(Key={'playerID':playerid})
    updatedPlayer = updatedPlayerRESP['Item']
    if 'win' in params:
        updatedPlayer['wins'] = updatedPlayer['wins'] + 1
    if 'lose' in params:
        updatedPlayer['loss'] = updatedPlayer['loss'] + 1
    playerDataBase.put_item(Item={
                                'playerID':playerid,
                                'wins':updatedPlayer['wins'],
                                'loss':updatedPlayer['loss'],
                                'skill':int(newSkill),
                                'ties':updatedPlayer['ties']
                            })
    return {
        'statusCode': 200,
        'body': json.dumps('Update Successful  player ID: '+updatedPlayer['playerID'])
    }