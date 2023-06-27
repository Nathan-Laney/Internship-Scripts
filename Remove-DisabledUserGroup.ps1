# Remove-DisabledUserGroup.ps1
# June 20th, 2023

# Written for Alexander County Government
# CONFIDENTIAL INFORMATION HAS BEEN REMOVED

# AUTHOR
# Nathan Laney
# Feel free to contact me at:
# nathaniel.laney@gmail.com

# This PowerShell script removes group membership from disabled users in the network. 
# This version of the script ignores ignored members. 

# Start logging (in C:\Temp\Remove-ADUsers.log)
Start-Transcript -Path C:\Temp\Remove-ADUsers.log -Append

# Import AD module (Not necessary if already installed locally)
# Import-ModuleActiveDirectory

# Input the IP of the DC you wish the script to run against 
# Script was run successfully on DC01 in our environment (as of June 20th, 2023)
$DC_IP = ""             # Holds an IP, for example "192.168.0.1"
$USERS_TO_REMOVE = ""   # Holds an OU, for example "OU=Disabled Users,DC=ExampleDomain,DC=local"
$OU_TO_IGNORE = ""      # Holds an OU, for example "OU=OU_to_ignore,OU=Example_Domain_Users,DC=ExampleDomain,DC=local"

# Create an ArrayList to hold all our Users we wish to iterate against
# ArrayList is used so we can easily remove ignored members
$users = [System.Collections.ArrayList]::new()
# Add all users from Disabled Users OU (ignored members have not yet been filtered out)
$users_unfiltered = Get-ADUser -Properties memberof,SamAccountName -Filter * -SearchBase $USERS_TO_REMOVE -Server $DC_IP
# Get all groups that are in ignored
$all_ignored_groups = Get-ADGroup -Filter * -SearchBase $OU_TO_IGNORE -SERVER $DC_IP 

# Recursively gets all members of the ignored OU or any child groups, and adds them to the $ignored_staff variable.
# This gets a complete list of ignored staff in order to cross-reference our Disabled Users against
$ignored_staff = foreach( $ignored_group in $all_ignored_groups ){ 
    Get-ADGroupMember -Identity $ignored_group -SERVER $DC_IP -Recursive | Select-Object -ExpandProperty SamAccountName | ForEach-Object {
        [pscustomobject]@{
            GroupName = $ignored_group.Name
            SamAccountName = $_
        }
    }
}

# Loop through our unfiltered list of disabled users, and filter out ignored members by cross-referencing the ignored staff group. 
foreach ($user in $users_unfiltered) {
    If ($ignored_staff.SamAccountName -contains $user.SamAccountName) {
        # ignored_member_groups is a string holding the membership of the specific user, to show which ignored groups they are in
        $ignored_member_groups = ""
        foreach ($ignored_listing in $ignored_staff){
            if($ignored_listing.SamAccountName -eq $user.SamAccountName){
                $ignored_member_groups += $ignored_listing.GroupName + ", "
            }
        }
        # If a ignored user is found, print out that they will be ignored. 
        Write-Host $user.Name "is a member of"$ignored_member_groups"and will not be processed. " -ForegroundColor DarkYellow
    } 
    # If they are not in ignored, 
    Else {
        # Add them to our filtered users and print that out
        $users.add($user) | out-null # out-null prevents printing of index
        Write-Host $user.Name " is not a member of ignored"                 #  This line can be removed to reduce logging if desired
    }
}

# For every user in our filtered list, 
foreach ($user in $users) {
    # for each of their groups, remove that user from that group. 
    foreach ($Group in (Get-ADUser $user -Properties MemberOf | Select-Object -ExpandProperty MemberOf)) { 
        
        # ------------------------------------------------------------------------------------------------------------ #
                    # ------------------------------- DANGER ZONE ------------------------------- #
        # ------------------------------------------------------------------------------------------------------------ #
        # This is the line that actually interacts with the AD. The -WhatIf tag means that the script will not 
        # remove any users, but instead just print out what it would do. Removing the -WhatIf tag will remove users.
        # ------------------------------------------------------------------------------------------------------------ #

        Remove-ADGroupMember -Members $user.DistinguishedName -Identity $Group -Confirm:$False -Server $DC_IP -WhatIf
        
        # ------------------------------------------------------------------------------------------------------------ #
        Write-Host "Disabled user " $user.Name " was a member of $Group and has been removed. " -ForegroundColor Green
    }
}

Write-Host "-----   COMPLETE    -----" -ForegroundColor Green