## UNDER MIT LICENSE

Copyright (C) 2011-2012 Leandro Voltolino <xupisco@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Python wrapper for Giantbomb API!

**Get your API Key at https://giantbomb.com/api/**

Basic usage:  

    import giantbomb  
    gb = giantbomb.Api('YOUR_KEY', 'YOUR_USER_AGENT')
    
**Current Methods:**  

 * search(str, offset)
 * get_game(game_id)
 * list_games(platform_id, offset)
 * get_platform(platform_id)
 * list_platforms(offset)
 
*Everything returns an object:*  

**Examples:**  

```python
from giantbomb import giantbomb
gb = giantbomb.Api('<YOUR API KEY>', 'API test')

# Search for games
search_results = gb.search('Jet Set Radio')
print(search_results)
# Outputs: [<20096: Jet Grind Radio>, <12117: JSRF: Jet Set Radio Future>, <40601: JetSet Secrets>, <17531: Jet Set Willy: Online>, <42406: Radio the Universe>, <5005: Jet Set Willy>, <2633: Jet>, <46238: Jet-Getters>, <73975: SoulSet>, <47155: Jet Gunner>]

# Get Game data
game_data = gb.get_game(20096)
print(game_data)
# Outputs: 

# List Platforms
platforms = gb.list_platforms()
print(platforms)
# Outputs: [<1: Amiga>, <3: Game Boy>, <4: Game Boy Advance>, <5: Game Gear>...]

# Get a specific platform
platform = gb.get_platform(37)
print(platform)
# Outputs: <37: Dreamcast>
```

Yep, that's it!  
Hugs!
