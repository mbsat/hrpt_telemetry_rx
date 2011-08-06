#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: USRP2 Meteor M-N1 HRPT Receiver
# Author: Martin Blaho
# Description: Receive, demodulate, bit synchronize, deframe and decode
# Generated: Sun Jul 24 11:32:25 2011
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import noaa
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
import poesweather
import wx

class usrp2_rx_mn1_hrpt_bb_fr(grc_wxgui.top_block_gui):

	def __init__(self, decim=50, gain=25, symb_rate=600*1109, baseband_file=os.environ['HOME'] + '/noaa_hrpt_baseband.dat', frames_file=os.environ['HOME'] + '/noaa_hrpt_frames.hmf', satellite='Meteor-M-N1', freq=1700e6, deframer_sync_check=True, pll_alpha=0.05, clock_alpha=0.05, deframer_insync_frames=4, deframer_outsync_frames=10):
		grc_wxgui.top_block_gui.__init__(self, title="USRP2 Meteor M-N1 HRPT Receiver")
		_icon_path = "/home/martin/.local/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Parameters
		##################################################
		self.decim = decim
		self.gain = gain
		self.symb_rate = symb_rate
		self.baseband_file = baseband_file
		self.frames_file = frames_file
		self.satellite = satellite
		self.freq = freq
		self.deframer_sync_check = deframer_sync_check
		self.pll_alpha = pll_alpha
		self.clock_alpha = clock_alpha
		self.deframer_insync_frames = deframer_insync_frames
		self.deframer_outsync_frames = deframer_outsync_frames

		##################################################
		# Variables
		##################################################
		self.decim_tb = decim_tb = decim
		self.symb_rate_tb = symb_rate_tb = symb_rate
		self.samp_rate = samp_rate = 100e6/decim_tb
		self.sps = sps = samp_rate/symb_rate_tb
		self.satellite_text = satellite_text = satellite
		self.samp_rate_st = samp_rate_st = samp_rate
		self.pll_alpha_sl = pll_alpha_sl = pll_alpha
		self.max_clock_offset = max_clock_offset = 0.1
		self.max_carrier_offset = max_carrier_offset = 2*math.pi*100e3/samp_rate
		self.hs = hs = int(sps/2.0)
		self.gain_tb = gain_tb = gain
		self.freq_tb = freq_tb = freq
		self.frames_file_text_inf = frames_file_text_inf = frames_file
		self.deframer_sync_after_text = deframer_sync_after_text = deframer_insync_frames
		self.deframer_nosync_after_text = deframer_nosync_after_text = deframer_outsync_frames
		self.deframer_check_sync_text = deframer_check_sync_text = deframer_sync_check
		self.datetime_text = datetime_text = strftime("%A, %B %d %Y %H:%M:%S", localtime())
		self.clock_alpha_sl = clock_alpha_sl = clock_alpha
		self.baseband_file_text_inf = baseband_file_text_inf = baseband_file

		##################################################
		# Blocks
		##################################################
		self.rx_ntb = self.rx_ntb = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "USRP Receiver")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "PLL demodulator and Clock sync")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "Deframer")
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
		_clock_alpha_sl_sizer = wx.BoxSizer(wx.VERTICAL)
		self._clock_alpha_sl_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_clock_alpha_sl_sizer,
			value=self.clock_alpha_sl,
			callback=self.set_clock_alpha_sl,
			label="Clock alpha",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._clock_alpha_sl_slider = forms.slider(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_clock_alpha_sl_sizer,
			value=self.clock_alpha_sl,
			callback=self.set_clock_alpha_sl,
			minimum=0.001,
			maximum=0.1,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.rx_ntb.GetPage(1).GridAdd(_clock_alpha_sl_sizer, 1, 1, 1, 1)
		self.wxgui_fftsink1 = fftsink2.fft_sink_c(
			self.rx_ntb.GetPage(0).GetWin(),
			baseband_freq=freq,
			y_per_div=5,
			y_divs=10,
			ref_level=50,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=30,
			average=True,
			avg_alpha=0.1,
			title="Not filtered spectrum",
			peak_hold=False,
		)
		self.rx_ntb.GetPage(0).Add(self.wxgui_fftsink1.win)
		self.usrp2_source_xxxx2_0 = usrp2.source_16sc()
		self.usrp2_source_xxxx2_0.set_decim(decim_tb)
		self.usrp2_source_xxxx2_0.set_center_freq(freq_tb)
		self.usrp2_source_xxxx2_0.set_gain(gain_tb)
		self._symb_rate_tb_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			value=self.symb_rate_tb,
			callback=self.set_symb_rate_tb,
			label="Symbol rate",
			converter=forms.int_converter(),
		)
		self.rx_ntb.GetPage(1).GridAdd(self._symb_rate_tb_text_box, 2, 1, 1, 1)
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
		self.poesweather_meteor_cadu_deframer_0 = poesweather.meteor_cadu_deframer(True, 256, deframer_insync_frames, deframer_outsync_frames)
		_pll_alpha_sl_sizer = wx.BoxSizer(wx.VERTICAL)
		self._pll_alpha_sl_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_pll_alpha_sl_sizer,
			value=self.pll_alpha_sl,
			callback=self.set_pll_alpha_sl,
			label="PLL Alpha",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._pll_alpha_sl_slider = forms.slider(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_pll_alpha_sl_sizer,
			value=self.pll_alpha_sl,
			callback=self.set_pll_alpha_sl,
			minimum=0.001,
			maximum=0.1,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.rx_ntb.GetPage(1).GridAdd(_pll_alpha_sl_sizer, 1, 0, 1, 1)
		self.pll = noaa.hrpt_pll_cf(pll_alpha_sl, pll_alpha_sl**2/4.0, max_carrier_offset)
		self.gr_vector_to_streams_0 = gr.vector_to_streams(gr.sizeof_short*1, 2)
		self.gr_short_to_float_0_0 = gr.short_to_float()
		self.gr_short_to_float_0 = gr.short_to_float()
		self.gr_multiply_const_vxx_0 = gr.multiply_const_vff((1, ))
		self.gr_moving_average_xx_0 = gr.moving_average_ff(hs, 1.0/hs, 4000)
		self.gr_float_to_complex_0 = gr.float_to_complex(1)
		self.gr_file_sink_0_1 = gr.file_sink(gr.sizeof_short*2, baseband_file)
		self.gr_file_sink_0_1.set_unbuffered(False)
		self.gr_file_sink_0_0 = gr.file_sink(gr.sizeof_char*1, frames_file)
		self.gr_file_sink_0_0.set_unbuffered(False)
		self.gr_clock_recovery_mm_xx_0 = gr.clock_recovery_mm_ff(sps/2.0, clock_alpha_sl**2/4.0, 0.5, clock_alpha_sl, max_clock_offset)
		self.gr_binary_slicer_fb_0 = gr.binary_slicer_fb()
		self.gr_agc_xx_0 = gr.agc_cc(10e-6, 1, 1.0/32767.0, 1.0)
		self._frames_file_text_inf_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(3).GetWin(),
			value=self.frames_file_text_inf,
			callback=self.set_frames_file_text_inf,
			label="Frames filename",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(3).GridAdd(self._frames_file_text_inf_static_text, 3, 0, 1, 1)
		self._deframer_sync_after_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(2).GetWin(),
			value=self.deframer_sync_after_text,
			callback=self.set_deframer_sync_after_text,
			label="Deframe sync after",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(2).GridAdd(self._deframer_sync_after_text_static_text, 3, 0, 1, 1)
		self._deframer_nosync_after_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(2).GetWin(),
			value=self.deframer_nosync_after_text,
			callback=self.set_deframer_nosync_after_text,
			label="Deframer out of sync after",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(2).GridAdd(self._deframer_nosync_after_text_static_text, 4, 0, 1, 1)
		self._deframer_check_sync_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(2).GetWin(),
			value=self.deframer_check_sync_text,
			callback=self.set_deframer_check_sync_text,
			label="Deframer check sync enable",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(2).GridAdd(self._deframer_check_sync_text_static_text, 2, 0, 1, 1)
		self._datetime_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(3).GetWin(),
			value=self.datetime_text,
			callback=self.set_datetime_text,
			label="Local time of aquisition start",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(3).GridAdd(self._datetime_text_static_text, 1, 0, 1, 1)
		self._baseband_file_text_inf_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(3).GetWin(),
			value=self.baseband_file_text_inf,
			callback=self.set_baseband_file_text_inf,
			label="Baseband filename",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(3).GridAdd(self._baseband_file_text_inf_static_text, 4, 0, 1, 1)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_float_to_complex_0, 0), (self.wxgui_fftsink1, 0))
		self.connect((self.pll, 0), (self.gr_moving_average_xx_0, 0))
		self.connect((self.gr_moving_average_xx_0, 0), (self.gr_clock_recovery_mm_xx_0, 0))
		self.connect((self.gr_agc_xx_0, 0), (self.pll, 0))
		self.connect((self.gr_float_to_complex_0, 0), (self.gr_agc_xx_0, 0))
		self.connect((self.gr_vector_to_streams_0, 0), (self.gr_short_to_float_0, 0))
		self.connect((self.gr_vector_to_streams_0, 1), (self.gr_short_to_float_0_0, 0))
		self.connect((self.usrp2_source_xxxx2_0, 0), (self.gr_vector_to_streams_0, 0))
		self.connect((self.usrp2_source_xxxx2_0, 0), (self.gr_file_sink_0_1, 0))
		self.connect((self.gr_short_to_float_0_0, 0), (self.gr_float_to_complex_0, 1))
		self.connect((self.gr_short_to_float_0, 0), (self.gr_float_to_complex_0, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.gr_binary_slicer_fb_0, 0))
		self.connect((self.gr_clock_recovery_mm_xx_0, 0), (self.gr_multiply_const_vxx_0, 0))
		self.connect((self.poesweather_meteor_cadu_deframer_0, 0), (self.gr_file_sink_0_0, 0))
		self.connect((self.gr_binary_slicer_fb_0, 0), (self.poesweather_meteor_cadu_deframer_0, 0))

	def get_decim(self):
		return self.decim

	def set_decim(self, decim):
		self.decim = decim
		self.set_decim_tb(self.decim)

	def get_gain(self):
		return self.gain

	def set_gain(self, gain):
		self.gain = gain
		self.set_gain_tb(self.gain)

	def get_symb_rate(self):
		return self.symb_rate

	def set_symb_rate(self, symb_rate):
		self.symb_rate = symb_rate
		self.set_symb_rate_tb(self.symb_rate)

	def get_baseband_file(self):
		return self.baseband_file

	def set_baseband_file(self, baseband_file):
		self.baseband_file = baseband_file
		self.set_baseband_file_text_inf(self.baseband_file)

	def get_frames_file(self):
		return self.frames_file

	def set_frames_file(self, frames_file):
		self.frames_file = frames_file
		self.set_frames_file_text_inf(self.frames_file)

	def get_satellite(self):
		return self.satellite

	def set_satellite(self, satellite):
		self.satellite = satellite
		self.set_satellite_text(self.satellite)

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self.set_freq_tb(self.freq)
		self.wxgui_fftsink1.set_baseband_freq(self.freq)

	def get_deframer_sync_check(self):
		return self.deframer_sync_check

	def set_deframer_sync_check(self, deframer_sync_check):
		self.deframer_sync_check = deframer_sync_check
		self.set_deframer_check_sync_text(self.deframer_sync_check)

	def get_pll_alpha(self):
		return self.pll_alpha

	def set_pll_alpha(self, pll_alpha):
		self.pll_alpha = pll_alpha
		self.set_pll_alpha_sl(self.pll_alpha)

	def get_clock_alpha(self):
		return self.clock_alpha

	def set_clock_alpha(self, clock_alpha):
		self.clock_alpha = clock_alpha
		self.set_clock_alpha_sl(self.clock_alpha)

	def get_deframer_insync_frames(self):
		return self.deframer_insync_frames

	def set_deframer_insync_frames(self, deframer_insync_frames):
		self.deframer_insync_frames = deframer_insync_frames
		self.set_deframer_sync_after_text(self.deframer_insync_frames)

	def get_deframer_outsync_frames(self):
		return self.deframer_outsync_frames

	def set_deframer_outsync_frames(self, deframer_outsync_frames):
		self.deframer_outsync_frames = deframer_outsync_frames
		self.set_deframer_nosync_after_text(self.deframer_outsync_frames)

	def get_decim_tb(self):
		return self.decim_tb

	def set_decim_tb(self, decim_tb):
		self.decim_tb = decim_tb
		self._decim_tb_text_box.set_value(self.decim_tb)
		self.set_samp_rate(100e6/self.decim_tb)
		self.usrp2_source_xxxx2_0.set_decim(self.decim_tb)

	def get_symb_rate_tb(self):
		return self.symb_rate_tb

	def set_symb_rate_tb(self, symb_rate_tb):
		self.symb_rate_tb = symb_rate_tb
		self.set_sps(self.samp_rate/self.symb_rate_tb)
		self._symb_rate_tb_text_box.set_value(self.symb_rate_tb)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.set_sps(self.samp_rate/self.symb_rate_tb)
		self.set_samp_rate_st(self.samp_rate)
		self.set_max_carrier_offset(2*math.pi*100e3/self.samp_rate)
		self.wxgui_fftsink1.set_sample_rate(self.samp_rate)

	def get_sps(self):
		return self.sps

	def set_sps(self, sps):
		self.sps = sps
		self.set_hs(int(self.sps/2.0))
		self.gr_clock_recovery_mm_xx_0.set_omega(self.sps/2.0)

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

	def get_pll_alpha_sl(self):
		return self.pll_alpha_sl

	def set_pll_alpha_sl(self, pll_alpha_sl):
		self.pll_alpha_sl = pll_alpha_sl
		self._pll_alpha_sl_slider.set_value(self.pll_alpha_sl)
		self._pll_alpha_sl_text_box.set_value(self.pll_alpha_sl)
		self.pll.set_alpha(self.pll_alpha_sl)
		self.pll.set_beta(self.pll_alpha_sl**2/4.0)

	def get_max_clock_offset(self):
		return self.max_clock_offset

	def set_max_clock_offset(self, max_clock_offset):
		self.max_clock_offset = max_clock_offset

	def get_max_carrier_offset(self):
		return self.max_carrier_offset

	def set_max_carrier_offset(self, max_carrier_offset):
		self.max_carrier_offset = max_carrier_offset
		self.pll.set_max_offset(self.max_carrier_offset)

	def get_hs(self):
		return self.hs

	def set_hs(self, hs):
		self.hs = hs
		self.gr_moving_average_xx_0.set_length_and_scale(self.hs, 1.0/self.hs)

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

	def get_frames_file_text_inf(self):
		return self.frames_file_text_inf

	def set_frames_file_text_inf(self, frames_file_text_inf):
		self.frames_file_text_inf = frames_file_text_inf
		self._frames_file_text_inf_static_text.set_value(self.frames_file_text_inf)

	def get_deframer_sync_after_text(self):
		return self.deframer_sync_after_text

	def set_deframer_sync_after_text(self, deframer_sync_after_text):
		self.deframer_sync_after_text = deframer_sync_after_text
		self._deframer_sync_after_text_static_text.set_value(self.deframer_sync_after_text)

	def get_deframer_nosync_after_text(self):
		return self.deframer_nosync_after_text

	def set_deframer_nosync_after_text(self, deframer_nosync_after_text):
		self.deframer_nosync_after_text = deframer_nosync_after_text
		self._deframer_nosync_after_text_static_text.set_value(self.deframer_nosync_after_text)

	def get_deframer_check_sync_text(self):
		return self.deframer_check_sync_text

	def set_deframer_check_sync_text(self, deframer_check_sync_text):
		self.deframer_check_sync_text = deframer_check_sync_text
		self._deframer_check_sync_text_static_text.set_value(self.deframer_check_sync_text)

	def get_datetime_text(self):
		return self.datetime_text

	def set_datetime_text(self, datetime_text):
		self.datetime_text = datetime_text
		self._datetime_text_static_text.set_value(self.datetime_text)

	def get_clock_alpha_sl(self):
		return self.clock_alpha_sl

	def set_clock_alpha_sl(self, clock_alpha_sl):
		self.clock_alpha_sl = clock_alpha_sl
		self._clock_alpha_sl_slider.set_value(self.clock_alpha_sl)
		self._clock_alpha_sl_text_box.set_value(self.clock_alpha_sl)
		self.gr_clock_recovery_mm_xx_0.set_gain_omega(self.clock_alpha_sl**2/4.0)
		self.gr_clock_recovery_mm_xx_0.set_gain_mu(self.clock_alpha_sl)

	def get_baseband_file_text_inf(self):
		return self.baseband_file_text_inf

	def set_baseband_file_text_inf(self, baseband_file_text_inf):
		self.baseband_file_text_inf = baseband_file_text_inf
		self._baseband_file_text_inf_static_text.set_value(self.baseband_file_text_inf)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("", "--decim", dest="decim", type="intx", default=50,
		help="Set Decimation [default=%default]")
	parser.add_option("", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(25),
		help="Set Gain [default=%default]")
	parser.add_option("", "--symb-rate", dest="symb_rate", type="intx", default=600*1109,
		help="Set Symbol rate [default=%default]")
	parser.add_option("", "--baseband-file", dest="baseband_file", type="string", default=os.environ['HOME'] + '/noaa_hrpt_baseband.dat',
		help="Set Baseband output filename [default=%default]")
	parser.add_option("", "--frames-file", dest="frames_file", type="string", default=os.environ['HOME'] + '/noaa_hrpt_frames.hmf',
		help="Set HRPT frames output filename [default=%default]")
	parser.add_option("", "--satellite", dest="satellite", type="string", default='Meteor-M-N1',
		help="Set Satellite [default=%default]")
	parser.add_option("", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(1700e6),
		help="Set Frequency [default=%default]")
	parser.add_option("", "--deframer-sync-check", dest="deframer_sync_check", type="intx", default=True,
		help="Set Deframer synchronisation check active [default=%default]")
	parser.add_option("", "--pll-alpha", dest="pll_alpha", type="eng_float", default=eng_notation.num_to_str(0.05),
		help="Set PLL alpha [default=%default]")
	parser.add_option("", "--clock-alpha", dest="clock_alpha", type="eng_float", default=eng_notation.num_to_str(0.05),
		help="Set Clock alpha [default=%default]")
	parser.add_option("", "--deframer-insync-frames", dest="deframer_insync_frames", type="intx", default=4,
		help="Set Count of valid ASM's after which deframer go in to synced state [default=%default]")
	parser.add_option("", "--deframer-outsync-frames", dest="deframer_outsync_frames", type="intx", default=10,
		help="Set Count of invalid ASM's after which deframer go out of synced state [default=%default]")
	(options, args) = parser.parse_args()
	tb = usrp2_rx_mn1_hrpt_bb_fr(decim=options.decim, gain=options.gain, symb_rate=options.symb_rate, baseband_file=options.baseband_file, frames_file=options.frames_file, satellite=options.satellite, freq=options.freq, deframer_sync_check=options.deframer_sync_check, pll_alpha=options.pll_alpha, clock_alpha=options.clock_alpha, deframer_insync_frames=options.deframer_insync_frames, deframer_outsync_frames=options.deframer_outsync_frames)
	tb.Run(True)

