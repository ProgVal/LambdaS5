param($scriptsDir, $xmlFilename)


function GetFilename($FullPathName) {
    $PIECES=$FullPathName.split(“\”) 
    $NUMBEROFPIECES=$PIECES.Count 
    $FILENAME=$PIECES[$NumberOfPieces-1] 
    return $FILENAME
} 


function ReplaceScript([string]$scriptCode, [xml]$testList, [string]$testID){
    $scriptCodeContent=""

    foreach($line in $scriptCode){
        $scriptCodeContent+=$line+"`r`n"
    }

    # remove comments
    $hs5HarnessPos=$scriptCodeContent.IndexOf("ES5Harness")
    $comments=$scriptCodeContent.Substring(0,$hs5HarnessPos) 
    $comments=$comments -replace "(//.*\n|/\*(.|\n)*?\*/)"
    $scriptCodeContent=$scriptCodeContent.Substring($hs5HarnessPos)
    $scriptCodeContent=[Convert]::ToBase64String($utf8Encoding.GetBytes($scriptCodeContent))
    $a = $testListFile.testCollection.section.test | Where-Object { $_.id -match $testID}
    $a.innerxml="<![CDATA["+$scriptCodeContent+"]]>"
}


 
$utf8Encoding = New-Object System.Text.UTF8Encoding


$testListFile=New-Object XML
$testListFile.load($xmlFilename)

if($scriptsDir.substring($scriptsDir.length-3,3) -match ".js") {
    $scriptCode=Get-Content -Encoding UTF8 $scriptsDir
    $testID = GetFilename $scriptsDir
    ReplaceScript $scriptCode $testListFile $testID.TrimEnd(".js")
}
else {
    $sourceFiles = get-childitem $scriptsDir -include *.js -recurse | where-object{$_.mode -notmatch "d"}
    foreach($test in $sourceFiles){
    $testName=$test.Name.Remove($test.Name.Length-3)
     if($testName.length -gt 0) { 
       $scriptCode=Get-Content -Encoding UTF8 $test.FullName
       ReplaceScript $scriptCode $testListFile $testName
      }
  }
}
$testListFile.Save($xmlFilename)
