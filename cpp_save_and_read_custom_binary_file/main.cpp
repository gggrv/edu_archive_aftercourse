/*--------------------------------------------------------------------------+++
* Script main.
* 
* https://www.tutorialspoint.com/reading-and-writing-binary-file-in-c-cplusplus
*/

// visual studio
#include <fstream>
#include <iostream>
#include <string>

// charity
//#include "utf8.h"

// same folder
#include "EntryFile.h"
#include "EntryIo.h"

void write_entry() {

    // create sample entry
    EntryFile ent;
    ent.set_text(
        "Artist : Colonel Claypool's Bucket of Bernie Brains\n"
        "Track Title : Ignorance is Bliss\n"
        "Album : The Big Eyeball in the Sky\n" );
    ent.add_bookmark( 0, 9,42, 0, "Artist" );
    ent.add_bookmark( 1, 66,18, 0, "Track Title" );
    ent.add_bookmark( 2, 0, "Local property1", "welcome" );

    // save the entry
    EntryIo writer;
    writer.save( "AAAAAAAAA.ede", ent );

    }

void read_entry() {

    // read entry
    EntryIo reader;
    EntryFile* ent = new EntryFile();
    bool success = reader.read( "AAAAAAAAA.ede", ent );

    std::vector<char> text = ent->get_text();
    for ( size_t iloc=0; iloc<text.size(); iloc+=1 ) {
        std::cout<< text[iloc];
        }

    }

/*--------------------------------------------------------------------------+++
* autorun.
*/

int main( int argc, char* argv[] ) {

    setlocale( LC_ALL, "" );

    write_entry();
    read_entry();

    std::cout<<"ok"<<std::endl;
    return 0;
    }//*/

//--------------------------------------------------------------------------+++
// „{„€„~„u„ˆ 2021.02.28 ¨ 2021.03.06