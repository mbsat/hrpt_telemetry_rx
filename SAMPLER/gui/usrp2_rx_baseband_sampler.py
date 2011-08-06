#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: USRP2 baseband sampler
# Author: Martin Blaho
# Description: USRP2 receive signal from antenna and save it to baseband file (ISHORT format)
# Generated: Tue Jul 26 20:51:14 2011
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import usrp2
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
from time import strftime, localtime, gmtime
import math, os
import wx

class usrp2_rx_baseband_sampler(grc_wxgui.top_block_gui):

	def __init__(self, gain=23, baseband_file=os.environ['HOME'] + '/GOES-LRIT_baseband.dat', decim=25, freq=137.50e6, satellite='SATxx'):
		grc_wxgui.top_block_gui.__init__(self, title="USRP2 baseband sampler")
		_icon_path = "/home/martin/.local/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Parameters
		##################################################
		self.gain = gain
		self.baseband_file = baseband_file
		self.decim = decim
		self.freq = freq
		self.satellite = satellite

		##################################################
		# Variables
		##################################################
		self.decim_tb = decim_tb = decim
		self.samp_rate = samp_rate = 100e6/decim_tb
		self.satellite_text = satellite_text = satellite
		self.samp_rate_st = samp_rate_st = samp_rate
		self.gain_tb = gain_tb = gain
		self.freq_tb = freq_tb = freq
		self.decimtext = decimtext = '_d'+str(decim)
		self.datetime_text = datetime_text = strftime("%A, %B %d %Y %H:%M:%S", localtime())
		self.baseband_file_text_inf = baseband_file_text_inf = baseband_file

		##################################################
		# Blocks
		##################################################
		self.rx_ntb = self.rx_ntb = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "USRP Receiver")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "Output")
		self.Add(self.rx_ntb)
		self._gain_tb_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.gain_tb,
			callback=self.set_gain_tb,
			label="RX gain [dB]",
			converter=forms.int_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._gain_tb_text_box, 1, 2, 1, 1)
		self._freq_tb_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.freq_tb,
			callback=self.set_freq_tb,
			label="Frequency",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._freq_tb_text_box, 1, 1, 1, 1)
		self._decim_tb_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.decim_tb,
			callback=self.set_decim_tb,
			label="Decimation",
			converter=forms.int_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._decim_tb_text_box, 1, 3, 1, 1)
		self.wxgui_fftsink1 = fftsink2.fft_sink_c(
			self.rx_ntb.GetPage(0).GetWin(),
			baseband_freq=freq,
			y_per_div=5,
			y_divs=10,
			ref_level=60,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=30,
			average=True,
			avg_alpha=0.1,
			title="USRP signal spectrum",
			peak_hold=False,
		)
		self.rx_ntb.GetPage(0).Add(self.wxgui_fftsink1.win)
		self.usrp2_source_xxxx2_0 = usrp2.source_16sc()
		self.usrp2_source_xxxx2_0.set_decim(decim_tb)
		self.usrp2_source_xxxx2_0.set_center_freq(freq_tb)
		self.usrp2_source_xxxx2_0.set_gain(gain_tb)
		self._satellite_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.satellite_text,
			callback=self.set_satellite_text,
			label="Sat ",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._satellite_text_static_text, 1, 0, 1, 1)
		self._samp_rate_st_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.samp_rate_st,
			callback=self.set_samp_rate_st,
			label="Sample rate",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._samp_rate_st_static_text, 1, 4, 1, 1)
		self.gr_vector_to_streams_0 = gr.vector_to_streams(gr.sizeof_short*1, 2)
		self.gr_short_to_float_0_0 = gr.short_to_float()
		self.gr_short_to_float_0 = gr.short_to_float()
		self.gr_float_to_complex_0 = gr.float_to_complex(1)
		self.gr_file_sink_0 = gr.file_sink(gr.sizeof_short*2, baseband_file)
		self.gr_file_sink_0.set_unbuffered(False)
		self._datetime_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			value=self.datetime_text,
			callback=self.set_datetime_text,
			label="Local time of aquisition start",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(1).GridAdd(self._datetime_text_static_text, 1, 0, 1, 1)
		self._baseband_file_text_inf_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			value=self.baseband_file_text_inf,
			callback=self.set_baseband_file_text_inf,
			label="Baseband filename",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(1).GridAdd(self._baseband_file_text_inf_static_text, 4, 0, 1, 1)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_vector_to_streams_0, 0), (self.gr_short_to_float_0, 0))
		self.connect((self.gr_short_to_float_0_0, 0), (self.gr_float_to_complex_0, 1))
		self.connect((self.gr_vector_to_streams_0, 1), (self.gr_short_to_float_0_0, 0))
		self.connect((self.gr_short_to_float_0, 0), (self.gr_float_to_complex_0, 0))
		self.connect((self.usrp2_source_xxxx2_0, 0), (self.gr_vector_to_streams_0, 0))
		self.connect((self.gr_float_to_complex_0, 0), (self.wxgui_fftsink1, 0))
		self.connect((self.usrp2_source_xxxx2_0, 0), (self.gr_file_sink_0, 0))

	def get_gain(self):
		return self.gain

	def set_gain(self, gain):
		self.gain = gain
		self.set_gain_tb(self.gain)

	def get_baseband_file(self):
		return self.baseband_file

	def set_baseband_file(self, baseband_file):
		self.baseband_file = baseband_file
		self.set_baseband_file_text_inf(self.baseband_file)

	def get_decim(self):
		return self.decim

	def set_decim(self, decim):
		self.decim = decim
		self.set_decim_tb(self.decim)
		self.set_decimtext('_d'+str(self.decim))

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self.set_freq_tb(self.freq)
		self.wxgui_fftsink1.set_baseband_freq(self.freq)

	def get_satellite(self):
		return self.satellite

	def set_satellite(self, satellite):
		self.satellite = satellite
		self.set_satellite_text(self.satellite)

	def get_decim_tb(self):
		return self.decim_tb

	def set_decim_tb(self, decim_tb):
		self.decim_tb = decim_tb
		self._decim_tb_text_box.set_value(self.decim_tb)
		self.set_samp_rate(100e6/self.decim_tb)
		self.usrp2_source_xxxx2_0.set_decim(self.decim_tb)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.set_samp_rate_st(self.samp_rate)
		self.wxgui_fftsink1.set_sample_rate(self.samp_rate)

	def get_satellite_text(self):
		return self.satellite_text

	def set_satellite_text(self, satellite_text):
		self.satellite_text = satellite_text
		self._satellite_text_static_text.set_value(self.satellite_text)

	def get_samp_rate_st(self):
		return self.samp_rate_st

	def set_samp_rate_st(self, samp_rate_st):
		self.samp_rate_st = samp_rate_st
		self._samp_rate_st_static_text.set_value(self.samp_rate_st)

	def get_gain_tb(self):
		return self.gain_tb

	def set_gain_tb(self, gain_tb):
		self.gain_tb = gain_tb
		self._gain_tb_text_box.set_value(self.gain_tb)
		self.usrp2_source_xxxx2_0.set_gain(self.gain_tb)

	def get_freq_tb(self):
		return self.freq_tb

	def set_freq_tb(self, freq_tb):
		self.freq_tb = freq_tb
		self._freq_tb_text_box.set_value(self.freq_tb)
		self.usrp2_source_xxxx2_0.set_center_freq(self.freq_tb)

	def get_decimtext(self):
		return self.decimtext

	def set_decimtext(self, decimtext):
		self.decimtext = decimtext

	def get_datetime_text(self):
		return self.datetime_text

	def set_datetime_text(self, datetime_text):
		self.datetime_text = datetime_text
		self._datetime_text_static_text.set_value(self.datetime_text)

	def get_baseband_file_text_inf(self):
		return self.baseband_file_text_inf

	def set_baseband_file_text_inf(self, baseband_file_text_inf):
		self.baseband_file_text_inf = baseband_file_text_inf
		self._baseband_file_text_inf_static_text.set_value(self.baseband_file_text_inf)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(23),
		help="Set Gain [default=%default]")
	parser.add_option("", "--baseband-file", dest="baseband_file", type="string", default=os.environ['HOME'] + '/GOES-LRIT_baseband.dat',
		help="Set Baseband output filename [default=%default]")
	parser.add_option("", "--decim", dest="decim", type="intx", default=25,
		help="Set Decimation [default=%default]")
	parser.add_option("", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(137.50e6),
		help="Set Frequency [default=%default]")
	parser.add_option("", "--satellite", dest="satellite", type="string", default='SATxx',
		help="Set Satellite [default=%default]")
	(options, args) = parser.parse_args()
	tb = usrp2_rx_baseband_sampler(gain=options.gain, baseband_file=options.baseband_file, decim=options.decim, freq=options.freq, satellite=options.satellite)
	tb.Run(True)

