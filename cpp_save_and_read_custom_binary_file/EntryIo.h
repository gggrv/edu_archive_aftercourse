#pragma once
/*--------------------------------------------------------------------------+++
* Script EntryIo.
* 
* Describes the EntryIo class.
* EntryIo writes and reads EntryFile objects from disk.
*/

// visual studio
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

// charity
//#include "utf8.h"

// same folder
#include "EntryFile.h"
#include "Bookmark.h"

class EntryIo {

    /*----------------------------------------------------------------------+++
    * Everything about file format.
    */
    public:
    const float WRITER_VERSION;
    const float READER_VERSION;

    /*----------------------------------------------------------------------+++
    * Everything about object construction/destruction.
    */
    public:

    // empty constructor
    EntryIo():
        // init list
        // file format
        WRITER_VERSION( 0.0 ),
        READER_VERSION( 0.0 ) {
        // constructor body
        }

    // destructor
    ~EntryIo() {
        // destructor body
        }

    /*----------------------------------------------------------------------+++
    * Everything about writing a file.
    */
    bool savefb( std::string path, EntryFile ent ) {
        // Writes binary part of ent to disk and reports whether
        // is was successful or not.
        /*------------------------------------------------------------------+++
        * Definitions.
        */

        // destination stream
        std::ofstream f( path, std::ios::out | std::ios::binary );

        // block sizes
        const size_t bookmarks_len( ent.bookmarks_len(false) );

        // bookmarks
        const size_t bookmarks_itemcount( ent.bookmarks_len(true) );

        // text
        const std::vector<char>* text_ptr = ent.text_addr();

        /*------------------------------------------------------------------+++
        * Actual code.
        */

        // access check
        if (!f) return false;

        // write file format
        f.write( reinterpret_cast<const char*>(&ent.MAGIC_NUMBER),
            sizeof(ent.MAGIC_NUMBER) );
        f.write( reinterpret_cast<const char*>(&ent.VERSION_NUMBER),
            sizeof(ent.VERSION_NUMBER) );
        f.write( reinterpret_cast<const char*>(&WRITER_VERSION),
            sizeof(WRITER_VERSION) );

        // write block sizes
        f.write( reinterpret_cast<const char*>(&bookmarks_len),
            sizeof(bookmarks_len) );
        f.write( reinterpret_cast<const char*>( &bookmarks_itemcount ),
            sizeof(bookmarks_itemcount) ); // how many of them i have
        for ( size_t iloc=0; iloc<bookmarks_itemcount; iloc+=1 ) {
            f.write( reinterpret_cast<const char*>(
                &((*ent.bookmarks_addr())[iloc]) ),
                sizeof( (*ent.bookmarks_addr())[iloc] )
            ); // write each one of them
            }

        // write text
        for ( size_t iloc=0; iloc<ent.text_len(true); iloc+=1 ) {
            char letter = (*text_ptr)[iloc];
            f.write( reinterpret_cast<const char*>(&letter),
                sizeof(letter) ); // char by char
            }

        f.close();

        // write check
        if ( !f.good() ) return false;

        return true;
        } // savefb...

    public:
    bool save( std::string path, EntryFile ent ) {
        // Writes ent to disk and reports whether
        // is was successful or not.

        bool success(false);
        success = savefb( path, ent );
        return success;

        }

    /*----------------------------------------------------------------------+++
    * Everything about reading a file.
    */
    private:
    bool readfb( std::string path, EntryFile* dummy_ob ) {
        // Reads binary part of an EntryFile into dummy_ob
        // and reports whether is was successful or not.
        /*------------------------------------------------------------------+++
        * Definitions.
        */

        // source stream
        std::ifstream f( path, std::ios::in | std::ios::binary );

        // file format
        char MAGIC_NUMBER[ sizeof(dummy_ob->MAGIC_NUMBER) ];

        // block sizes
        size_t bookmarks_len(0);

        // bookmarks
        size_t bookmarks_itemcount(0);

        /*------------------------------------------------------------------+++
        * Actual code.
        */

        // access check
        if (!f) return false;

        // magic number check
        f.read( (char*)&MAGIC_NUMBER, sizeof(MAGIC_NUMBER) );
        for ( size_t iloc=0; iloc<sizeof(MAGIC_NUMBER); iloc+=1 ) {
            if (MAGIC_NUMBER[iloc]!=dummy_ob->MAGIC_NUMBER[iloc]) return false;
            }

        // read file format
        f.read( (char*)&dummy_ob->VERSION_NUMBER,
            sizeof(dummy_ob->VERSION_NUMBER));
        f.read( (char*)&dummy_ob->WRITER_VERSION,
            sizeof(dummy_ob->WRITER_VERSION));

        // read block sizes
        f.read( (char*)&bookmarks_len, sizeof(bookmarks_len) );

        // read bookmarks
        f.read( (char*)&bookmarks_itemcount,
            sizeof(bookmarks_itemcount) ); // how many of them i have
        for ( size_t iloc=0; iloc<bookmarks_itemcount; iloc+=1 ) {

            // read data into placeholder array
            char dest[ sizeof(Bookmark) ];
            char* dest_ptr = dest;
            f.read( dest_ptr, sizeof(dest) ); // read each one of them

            // manually reinterpret read binary data
            Bookmark bookmark = 
                *reinterpret_cast<Bookmark*>(dest_ptr);
            dummy_ob->add_bookmark( bookmark );
            }

        // get text size
        std::streamoff sta( f.tellg() );
        f.seekg( 0, std::ios::end );
        std::streamoff end( f.tellg() );
        f.seekg( sta, std::ios::beg );
        size_t len( end-sta );

        // read text
        std::vector<char> dest(len);
        f.read( &dest[0], len );
        dummy_ob->set_text( dest );

        f.close();

        return true;
        } // readfb...

    public:
    bool read( std::string path, EntryFile* dummy_ob ) {
        // Reads an EntryFile from disk into the dummy_ob
        // and reports whether is was successful or not.

        bool success(false);
        success = readfb( path, dummy_ob );

        // assign reader version to the file
        dummy_ob->READER_VERSION = READER_VERSION;

        return success;

        }

    }; // class EntryIo...

//--------------------------------------------------------------------------+++
// Ñ{ÑÄÑ~ÑuÑà 2021.02.28 Å® 2021.03.05