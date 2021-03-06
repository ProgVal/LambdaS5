import datetime
import os
import subprocess
import sys
import time
import argparse

from single_test import *

result_dir = "results-test"

def testFile(useC3, f):
  def mkRow(typ, message):
    return "<li class='%s'><a href='%s'>%s</a>%s</li>" % \
      (typ, str(f), str(f), message)

  print(str(f))
  parsed = parse(useC3, buildHarnessed(open(f)))
  if parsed == "ParseError":
    return (mkRow('skipped', " (ParseError)"), 0, 0, 1, 0, 0)

  (typ, stdout, stderr) = run(useC3, parsed)
  strict = 0
  if not (stdout is None) and (stdout.find("STRICT TEST") != -1):
    strict = 1

  if typ == "Timeout":
    return (mkRow('failed', " (Timed out)"), 0, 1, 0, 0, strict)
  elif typ == "With":
    return (mkRow('skipped', " (With)"), 0, 0, 1, 0, 0)
  elif typ == "Success":
    return (mkRow('passed', ""), 1, 0, 0, strict, 0)
  else: # typ is "Failure"
    return ("<li class='failed'><div><a href='%s'>%s</a> (Failed)</div> \
              <div>Type:%s</div> \
              <div>Stdout:</div> \
              <p>%s</p> \
              <div>Stderr:</div> \
              <p>%s</p> \
            </li>" % (str(f), str(f), typ, stdout, stderr), 0, 1, 0, 0, strict)

def testDir(useC3, d):
  files = os.listdir(str(d))
  inner = ""
  passed = 0
  failed = 0
  skipped = 0
  spassed = 0
  sfailed = 0
  for f in files:
    f = os.path.join(str(d), f)
    if(os.path.isdir(f)):
      (fHtml, fPassed, fFailed, fSkipped, fsPassed, fsFailed) = testDir(useC3, f)
    else:
      (fHtml, fPassed, fFailed, fSkipped, fsPassed, fsFailed) = testFile(useC3, f)
    passed += fPassed
    failed += fFailed
    spassed += fsPassed
    sfailed += fsFailed
    skipped += fSkipped
#    try:
	    #      inner += fHtml
#    finally:
    inner += "<div>Skipped for parsing reasons</div>"

  color = 'failed'
  if failed == 0:
    color = 'passed'

  return ("<li class='%s'>%s; %s passed, %s failed (strict %s passed, %s failed), \
          <a href='#' class='toggle'>(show/hide)</a> \
          <ul class='showing'>%s</ul></li>" % (color, str(d), passed, failed, spassed, sfailed, inner),
          passed,
          failed,
          skipped,
          spassed,
          sfailed)

template = """
<html>
<head>
<style type='text/css'>
ul {
  margin: 1ex;
}

li {
  border: 2px solid black;
  padding: 1ex;
}

ul.showing {
  display: block
}

ul.hidden {
  display: none
}

li.passed {
  background: #99FF66;
}

li.skipped {
  background: #CCCCFF;
}

li.failed {
  background: #FF9999;
}
</style>
<script>
window.addEventListener('load', function(e) {
  var elts = document.getElementsByClassName('toggle');
  for (var i = 0; i < elts.length; i++) {
    var elt = elts[i];
    elt.addEventListener('click', (function(elt){
      return function(e) {
        var uls = elt.parentNode.getElementsByTagName("ul");
        for (var j = 0; j < uls.length; j++) {
          var ul = uls[j];
          if(ul.className === 'showing') ul.className = 'hidden';
          else ul.className = 'showing';
        }
        e.preventDefault();
      }
    })(elt));
  }
});
</script>
</head>

<body>
  <ul>
    %s
  </ul>
</body>
</html>
"""

def usage():
  print("""
    python all-tests.py <ie | sp> <dir1 dir2 ...>

      When run with no arguments, will run all the tests in ietestcenter
      and in sputnik_converted.

      If the first argument is ie, it will run the directories listed
      within the ietestcenter tests.  If the first argument is sp, it will
      run all the sputnik tests.

      If the first argument is regen, it will recreate summary.html with
      whatever information it finds in the test directory.
  """)

def dirTests(useC3, d):
  for chapter in os.listdir(d):
    f = open(os.path.join(result_dir, chapter + ".html"), "w")
    f2 = open(os.path.join(result_dir, chapter + ".result"), "w")
    result = testDir(useC3, os.path.join(d, chapter))
    f.write(template % result[0])
    f2.write("%s %s %s %s %s" % result[1:])

def makeFrontPage():
  html = """
<html><head></head>
Tests run at %s
<ul>%s</ul><div>Total: %s/%s (%s/%s) [%s skipped]</div></html>
"""
  l = ""
  totalS = 0
  totalF = 0
  totalSk = 0
  totalSs = 0
  totalSf = 0
  for chapter in sorted(os.listdir(result_dir)):
    if chapter[-6:] == 'result':
      print("Result dir: %s\nChapter:%s\n" % (result_dir, chapter))
      line = open(os.path.join(result_dir, chapter)).readline()
      if line and len(line) == 4: [success, fail, skip, ssuccess, sfail] = line.split(" ")
      else: continue
      l += "<li><a href='%s.html'>%s</a> (%s/%s), (%s/%s)</li>" % \
              (chapter[0:-7], chapter[0:-7], success, int(success)+int(fail), \
               ssuccess, int(ssuccess) + int(sfail))
      totalS += int(success)
      totalF += int(fail)
      totalSk += int(skip)
      totalSs += int(ssuccess)
      totalSf += int(sfail)

  summary = open(os.path.join(result_dir, "summary.html"), "w")
  summary.write(html % (str(datetime.datetime.now()), l, totalS, totalS + totalF, totalSs, totalSf, totalSk))
  summary.close()

def main(args):
  spiderMonkeyDir = 'test262/test/suite/converted/'
  ieDir = 'test262/test/suite/converted/'
  try:
    os.mkdir(result_dir)
  except:
    # silent fail, the directory probably already existed
    # (couldn't find mkdir -p equivalent)
    pass

  argparser = argparse.ArgumentParser(description='Launch all test262 tests')
  argparser.add_argument("action", choices = ["all", "sp", "ie", "regen"])
  argparser.add_argument("-c3", action='store_true')
  argparser.add_argument("chapters", nargs="*")

  args = argparser.parse_args()

  if args.action == "all":
    dirTests(args.c3, spiderMonkeyDir)
    dirTests(args.c3, ieDir)
  else:
    if (args.action == "regen"): makeFrontPage(); return
    elif (args.action == "sp"): d = spiderMonkeyDir
    else: d = ieDir

    for chapter in args.chapters:
      print("doing a chapter: %s" % chapter)
      f = open(os.path.join(result_dir, chapter + ".html"), "w")
      f2 = open(os.path.join(result_dir, chapter + ".result"), "w")
      result = testDir(args.c3, os.path.join(d, chapter))
      f.write(template % result[0])
      f2.write("%s %s %s %s %s" % result[1:])
      f.close()
      f2.close()

  makeFrontPage()

main(sys.argv)

