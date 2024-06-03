# Import the Active Directory module
Import-Module ActiveDirectory

# Define the computer name
$computerName = "YourComputerName"

# Retrieve the computer object from AD and its userCertificate attribute
$computer = Get-ADComputer -Identity $computerName -Properties userCertificate

# Initialize an array to store the certificate information
$certificateDetails = @()

# Check if the computer has certificates
if ($computer.userCertificate -ne $null) {
    foreach ($certBlob in $computer.userCertificate) {
        # Decode the certificate
        $cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2
        $cert.Import($certBlob)

        # Create a custom object to store certificate details
        $certInfo = [PSCustomObject]@{
            ComputerName = $computerName
            Subject = $cert.Subject
            Issuer = $cert.Issuer
            Thumbprint = $cert.Thumbprint
            NotBefore = $cert.NotBefore
            NotAfter = $cert.NotAfter
            Status = if ($cert.NotAfter -gt (Get-Date)) { "Valid" } else { "Expired" }
        }

        # Add the certificate details to the array
        $certificateDetails += $certInfo
    }

    # Export the certificate details to a CSV file
    $csvPath = "C:\Path\To\Export\$computerName-certificates.csv"
    $certificateDetails | Export-Csv -Path $csvPath -NoTypeInformation
    Write-Host "Certificate details exported to $csvPath"
} else {
    Write-Host "No certificates found for $computerName"
}