from __future__ import division
from decorate import main
from datetime import timedelta
import sys
import time

the_scr=None

cakeimg="""                  {}
                  ||
              ____||_____
         {}  {~ ~ ~ ~ ~ ~}  {}
         ||  { ~ ~ ~ ~ ~ }  ||
       __||__{___________}__||__
      {\/\/\/\/\/\/\/\/\/\/\/\/\}
   {} {                        \} {}
   || {\/\/\/\/\/\/\/\/\/\/\/\/\} ||
 __||_{_________________________}_||__
{\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\}
{                                     }
{                                     }
{                                     }
{/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/}
{_____________________________________}"""

smiley='''                          oooo$$$$$$$$$$$$oooo
                      oo$$$$$$$$$$$$$$$$$$$$$$$$o
                   oo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$o         o$   $$ o$
   o $ oo        o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$o       $$ $$ $$o$
oo $ $ "$      o$$$$$$$$$    $$$$$$$$$$$$$    $$$$$$$$$o       $$$o$$o$
"$$$$$$o$     o$$$$$$$$$      $$$$$$$$$$$      $$$$$$$$$$o    $$$$$$$$
  $$$$$$$    $$$$$$$$$$$      $$$$$$$$$$$      $$$$$$$$$$$$$$$$$$$$$$$
  $$$$$$$$$$$$$$$$$$$$$$$    $$$$$$$$$$$$$    $$$$$$$$$$$$$$  """$$$
   "$$$""""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     "$$$
    $$$   o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     "$$$o
   o$$"   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       $$$o
   $$$    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$" "$$$$$$ooooo$$$$o
  o$$$oooo$$$$$  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   o$$$$$$$$$$$$$$$$$
  $$$$$$$$"$$$$   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     $$$$""""""""
 """"       $$$$    "$$$$$$$$$$$$$$$$$$$$$$$$$$$$"      o$$$
            "$$$o     """$$$$$$$$$$$$$$$$$$"$$"         $$$
              $$$o          "$$""$$$$$$""""           o$$$
               $$$$o                                o$$$"
                "$$$$o      o$$$$$$o"$$$$o        o$$$$
                  "$$$$$oo     ""$$$$o$$$$$o   o$$$$""
                     ""$$$$$oooo  "$$$o$$$$$$$$$"""
                        ""$$$$$$$oo $$$$$$$$$$
                                """"$$$$$$$$$$$
                                    $$$$$$$$$$$$
                                     $$$$$$$$$$"
                                      "$$$""                               '''

def fmt_time(t, delimiters):
    """Return time formatted as a timedelta object."""
    meta_t = timedelta(seconds=round(t))
    return ''.join([delimiters[0], str(meta_t), delimiters[1]])

def _progress(percent, style, layout):
    # percentage string
    percent_s = "%3d%%" % int(round(percent*100))
    if style == 'bar':
        # how many symbols for such percentage
        symbols = int(round(percent * layout['width']))
        # build percent done arrow
        done = ''.join([layout['char1']*(symbols), layout['char2']])
        # build remaining space
        todo = ''.join([layout['char3']*(layout['width']-symbols)])
        # build the progress bar
        box =  ''.join([layout['delimiters'][0],
                        done, todo,
                        layout['delimiters'][1]])
        if layout['position'] == 'left':
            # put percent left
            box = ''.join(['\r', layout['indent'], percent_s, box])
        elif layout['position'] == 'right':
            # put percent right
            box = ''.join(['\r', layout['indent'], box, percent_s])
        else:
            # put it in the center
            percent_s = percent_s.lstrip()
            percent_idx = (len(box) // 2) - len(percent_s) + 2
            box = ''.join(['\r', layout['indent'],
                           box[0:percent_idx],
                           percent_s,
                           box[percent_idx+len(percent_s):]])
    elif style == 'timer':
        now = time.time()
        if percent == 0:
            # write the time box directly
            tbox = ''.join(['?', layout['separator'], '?'])
        else:
            # Elapsed
            elapsed = now - layout['t_start']
            # Estimated total time
            if layout['speed'] == 'mean':
                e_t_a = elapsed/percent - elapsed
            else:
                # instantaneous speed
                progress = percent-_progress.last_percent
                e_t_a = (1 - percent)/progress*(now-_progress.last_time)
            # build the time box
            tbox = ''.join([fmt_time(elapsed, layout['delimiters']),
                            layout['separator'],
                            fmt_time(e_t_a, layout['delimiters'])])
        # compose progress info box
        if layout['position'] == 'left':
            box = ''.join(['\r',
                           layout['indent'],
                           percent_s,
                           ' ',
                           tbox])
        else:
            box = ''.join(['\r',
                           layout['indent'],
                           tbox,
                           ' ',
                           percent_s])

        _progress.last_percent = percent
        _progress.last_time = now
    elif style == 'img_stack':
        lines = layout['image'].splitlines()
        # how many symbols for such percentage
        symbols = int(round(percent * len(lines)))
        empty = ' '*len(lines[-1])
        building = '^'*len(lines[-1])
        done = '\n'.join(lines[len(lines)-symbols:])
        x = [empty]*(len(lines)-symbols)
        if len(x) > 0:
            x[-1] = building
        todo = '\n'.join(x)
        box =  '\n'.join([todo, done])
    return box

def pcake(percent):
    symbols = int(round(percent * len(cakelines)))
    empty = ' '*len(cakelines[-1])
    building = '^'*len(cakelines[-1])
    done = '\n'.join(cakelines[len(cakelines)-symbols:])
    x = [empty]*(len(cakelines)-symbols)
    if len(x) > 0:
        x[-1] = building
    todo = '\n'.join(x)
    box =  '\n'.join([todo, done])
    print box

def progressinfo(sequence, length = None, style = 'bar', custom = None):
    iterate_on_items = False
    # try to get the length of the sequence
    try:
        length = len(sequence)
    # if the object is unsized
    except TypeError:
        if length is None:
            err_str = "Must specify 'length' if sequence is unsized."
            raise Exception(err_str)
        elif length < 0:
            iterate_on_items = True
            length = -length
    length = float(length)
    # set layout
    if style == 'bar':
        layout = { 'indent': '',
                   'width' : the_scr.getmaxyx()[1],
                   'position' : 'middle',
                   'delimiters' : '[]',
                   'char1' : '=',
                   'char2' : '>',
                   'char3' : '.' }
        if custom is not None:
            layout.update(custom)
        fixed_lengths = len(layout['indent']) + 4
        if layout['position'] in ['left', 'right']:
            fixed_lengths += 4
        layout['width'] = layout['width'] - fixed_lengths
    elif style == 'timer':
        layout = { 'speed': 'mean',
                   'indent': '',
                   'position' : 'left',
                   'delimiters' : '[]',
                   'separator': ' - ',
                   't_start' : time.time()
                   }
        if custom is not None:
            layout.update(custom)
    elif style == 'img_stack':
        layout = dict(image=cakeimg)
        if custom is not None:
            layout.update(custom)
    else:
        err_str = "Style `%s' not known." % style
        raise ValueError(err_str)

    # start main loop
    last = None
    for count, value in enumerate(sequence):
        # generate progress info
        if iterate_on_items:
            box = _progress(value/length, style, layout)
        else:
            box = _progress(count/length, style, layout)
        # print it only if something changed from last time
        if box != last:
            the_scr.addstr(5,0, box)
            the_scr.refresh()
            last = box
        yield value
    else:
        # we need this for the 100% notice
        if iterate_on_items:
            box = _progress(1., style, layout)
        else:
            box = _progress((count+1)/length, style, layout)
        if box != last:
            the_scr.addstr(5,0, box)
            the_scr.refresh()
            last = box

testit_src = """
def testit():
    global the_scr
    from curses_test import curseswin
    with curseswin() as scr:
        scr.nodelay(True)
        the_scr = scr
        # scr.addstr(5,0,_progress(0/200, style="cake", layout={}))
        # scr.refresh()
            # time.sleep(.01)
        for i in progressinfo(range(200),style='img_stack',
            custom={'image':testit_src}):
            c = scr.getch()
            if c == ord('q'):
                return
            elif c == ord(' '):
                while 1:
                    c = scr.getch()
                    if c == ord('q'): return
                    elif c == ord(' '): break
            time.sleep(.05)
        while 1:
            c = scr.getch()
            if c == ord('q'): return
"""


progopts = {
    'bar':['bar',{}],
    'cake':['img_stack',dict(image=cakeimg)],
    'smile':['img_stack',dict(image=smiley)],
    'john':['img_stack',dict(image=open('face.txt').read())],
    'timer':['timer',{}],
}

@main
def testit(which='bar'):
    global the_scr
    from curses_test import curseswin
    style, layout = progopts.get(which, ['bar',{}])
    with curseswin() as scr:
        scr.nodelay(True)
        the_scr = scr
        for i in progressinfo(range(200),style=style,custom=layout):
            c = scr.getch()
            if c == ord('q'):
                return
            elif c == ord(' '):
                while 1:
                    c = scr.getch()
                    if c == ord('q'): return
                    elif c == ord(' '): break
            time.sleep(.02)
        while 1:
            c = scr.getch()
            if c == ord('q'): return
    

# if __name__ == '__main__':
    # testit()
    # pcake(0)
    # print _progress(200/200, style="cake", layout={})