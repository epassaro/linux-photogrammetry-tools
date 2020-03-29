#! /bin/bash

get_sift () {
  echo
  wget -q --show-progress http://www.cs.ubc.ca/~lowe/keypoints/siftDemoV4.zip
  unzip -qq siftDemoV4
  cp siftDemoV4/sift bin/
  cp siftDemoV4/LICENSE bin/
  rm siftDemoV4.zip
  rm -r siftDemoV4
  echo; echo
  echo "Finished."
}

echo "LICENSE CONDITIONS

Copyright (2005), University of British Columbia.

This software for the detection of invariant keypoints is being made
available for individual research use only.  Any commercial use or any
redistribution of this software requires a license from the University
of British Columbia.

The following patent has been issued for methods embodied in this
software: \"Method and apparatus for identifying scale invariant
features in an image and use of same for locating an object in an
image,\" David G. Lowe, US Patent 6,711,293 (March 23,
2004). Provisional application filed March 8, 1999. Asignee: The
University of British Columbia.

For further details on obtaining a commercial license, contact David
Lowe (lowe@cs.ubc.ca) or the University-Industry Liaison Office of the
University of British Columbia. 

THE UNIVERSITY OF BRITISH COLUMBIA MAKES NO REPRESENTATIONS OR
WARRANTIES OF ANY KIND CONCERNING THIS SOFTWARE.

This license file must be retained with all copies of the software,
including any modified or derivative versions."
echo; echo

while true; do
    read -p "Do you agree to the above license terms? " yn
    case $yn in
        [Yy]* ) get_sift; break;;
        [Nn]* ) exit 1;;
        * ) echo "Please answer yes or no.";;
    esac
done

exit 0





exit 0



