#pragma once
/*--------------------------------------------------------------------------+++
* Script EntryFile.
* 
* Describes the EntryFile class.
*/
/*--------------------------------------------------------------------------+++
* TODO.
* 
* auto assign ilocs to bookmarks within a single file
* auto verify those ilocs
* auto track holes in ilocs after deleting bookmarks
* 
* delete bookmarks
* 
*/

// visual studio
#include <iostream>
#include <string>
#include <vector>

// same folder
#include "Bookmark.h"

class EntryFile {

    /*----------------------------------------------------------------------+++
    * Everything about bookmarks definitions.
    */
    private:
    std::vector<Bookmark> BOOKMARKS;

    /*----------------------------------------------------------------------+++
    * Everything about text definitions.
    */
    private:
    std::vector<char> TEXT;

    /*----------------------------------------------------------------------+++
    * Everything about file format.
    */
    public:
    const char MAGIC_NUMBER[13];
    float VERSION_NUMBER;
    float WRITER_VERSION;
    float READER_VERSION;

    /*----------------------------------------------------------------------+++
    * Everything about object construction/destruction.
    */
    public:

    // empty constructor
    EntryFile():
        // init list
        // file format
        MAGIC_NUMBER( "desert years" ),
        VERSION_NUMBER( 0.1 ),
        WRITER_VERSION( 0.0 ),
        READER_VERSION( 0.0 ),
        // file content
        BOOKMARKS( std::vector<Bookmark>() ),
        TEXT() {
        // constructor body
        }

    // constructor with all values
    EntryFile(
        std::vector<Bookmark> bookmarks,
        std::string text ):
        // init list
        // file format
        MAGIC_NUMBER( "desert years" ),
        VERSION_NUMBER( 0.1 ),
        WRITER_VERSION( 0.0 ),
        READER_VERSION( 0.0 ),
        // file content
        BOOKMARKS(bookmarks),
        TEXT( text.size() ) {
        // constructor body

        // initialize text
        this->TEXT.assign( text.cbegin(), text.cend() );

        }

    // destructor
    ~EntryFile() {
        // destructor body
        }

    /*----------------------------------------------------------------------+++
    * Everything about complex data.
    */
    public:

    // adding bookmarks
    void add_bookmark(
        size_t iloc, size_t sta, size_t len, size_t conn,
        std::string label ) {
        // adds visible (in-text)
        Bookmark item( iloc,sta,len,conn,label );
        this->BOOKMARKS.push_back( item );
        }
    void add_bookmark(
        size_t iloc, size_t conn,
        std::string label, std::string value ) {
        // adds invisible (just value)
        Bookmark item( iloc,conn,label,value );
        this->BOOKMARKS.push_back( item );
        }
    void add_bookmark( Bookmark item ) {
        // adds existing object
        this->BOOKMARKS.push_back( item );
        }

    // getting bookmarks
    std::vector<Bookmark> get_bookmarks() {
        return this->BOOKMARKS;
        }

    // util
    size_t bookmarks_len( bool itemcount=false ) {
        // Returns the size of bookmarks in this file.
        // In bytes or as itemcount.
        if (itemcount) { return this->BOOKMARKS.size(); }
        return sizeof( this->BOOKMARKS );
        }
    std::vector<Bookmark>* bookmarks_addr() {
        return &this->BOOKMARKS;
        }

    /*----------------------------------------------------------------------+++
    * Everything about text.
    */
    public:

    // set text
    void set_text( std::string text ) {
        this->TEXT.assign( text.cbegin(), text.cend() );
        }
    void set_text( std::vector<char> text ) {
        this->TEXT = text;
        }

    // remove current text
    void clear_text() {
        this->TEXT.clear();
        }

    // get current text
    std::vector<char> get_text() {
        return this->TEXT;
        }

    // util
    size_t text_len( bool itemcount=false ) {
        // Returns the size of text in this file.
        // In bytes or as itemcount.
        if (itemcount) { return this->TEXT.size(); }
        return sizeof( this->TEXT );
        }
    std::vector<char>* text_addr() {
        return &this->TEXT;
        }

    }; // class EntryFile...

//--------------------------------------------------------------------------+++
// Ñ{ÑÄÑ~ÑuÑà 2021.03.02 Å® 2021.03.05