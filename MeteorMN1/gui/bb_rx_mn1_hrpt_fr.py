#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Meteor M-N1 HRPT Receiver from baseband file
# Author: Martin Blaho
# Description: From BB file demodulate, bit synchronize, deframe and decode
# Generated: Sun Jul 24 11:58:50 2011
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import noaa
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
from time import strftime, localtime, gmtime
import math, os
import poesweather
import wx

class bb_rx_mn1_hrpt_fr(grc_wxgui.top_block_gui):

	def __init__(self, decim=50, satellite='Meteor-M-N1', frames_file=os.environ['HOME'] + '/MN1_hrpt_frames.hmf', baseband_file="/home/martin/GNURadioData/hrpt/baseband/HRPT_Meteor-M-N1_2011-02-27_09-30-46_UTC_U2_d50.sam", symb_rate=600*1109, clock_alpha=0.050, pll_alpha=0.05, deframer_outsync_frames=100, deframer_insync_frames=3, deframer_sync_check=False):
		grc_wxgui.top_block_gui.__init__(self, title="Meteor M-N1 HRPT Receiver from baseband file")
		_icon_path = "/home/martin/.local/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Parameters
		##################################################
		self.decim = decim
		self.satellite = satellite
		self.frames_file = frames_file
		self.baseband_file = baseband_file
		self.symb_rate = symb_rate
		self.clock_alpha = clock_alpha
		self.pll_alpha = pll_alpha
		self.deframer_outsync_frames = deframer_outsync_frames
		self.deframer_insync_frames = deframer_insync_frames
		self.deframer_sync_check = deframer_sync_check

		##################################################
		# Variables
		##################################################
		self.decim_tb = decim_tb = decim
		self.symb_rate_tb = symb_rate_tb = symb_rate
		self.samp_rate = samp_rate = 100e6/decim_tb
		self.sps = sps = samp_rate/symb_rate_tb
		self.v = v = True
		self.satellite_text = satellite_text = satellite
		self.samp_rate_st = samp_rate_st = samp_rate
		self.pll_alpha_sl = pll_alpha_sl = pll_alpha
		self.max_clock_offset = max_clock_offset = 0.1
		self.max_carrier_offset = max_carrier_offset = 2*math.pi*100e3/samp_rate
		self.hs = hs = int(sps/2.0)
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
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "Input baseband")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "PLL demodulator and Clock sync")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "Deframer")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "Output")
		self.Add(self.rx_ntb)
		self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
			self.GetWin(),
			title="Scope Plot",
			sample_rate=samp_rate,
			v_scale=0,
			v_offset=0,
			t_scale=0,
			ac_couple=False,
			xy_mode=False,
			num_inputs=1,
			trig_mode=gr.gr_TRIG_MODE_AUTO,
			y_axis_label="Counts",
		)
		self.Add(self.wxgui_scopesink2_0.win)
		self.wxgui_fftsink1 = fftsink2.fft_sink_c(
			self.rx_ntb.GetPage(0).GetWin(),
			baseband_freq=0,
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
		self._v_check_box = forms.check_box(
			parent=self.GetWin(),
			value=self.v,
			callback=self.set_v,
			label="Open",
			true=True,
			false=False,
		)
		self.Add(self._v_check_box)
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
		self.poesweather_meteor_cadu_deframer_0 = poesweather.meteor_cadu_deframer(deframer_sync_check, 256, deframer_insync_frames, deframer_outsync_frames)
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
		self.pll = noaa.hrpt_pll_cf(pll_alpha, pll_alpha**2/4.0, max_carrier_offset)
		self.gr_throttle_0 = gr.throttle(gr.sizeof_short*1, samp_rate*10)
		self.gr_multiply_const_vxx_0 = gr.multiply_const_vff((-1, ))
		self.gr_moving_average_xx_0 = gr.moving_average_ff(hs, 1.0/hs, 4000)
		self.gr_file_source_0_0 = gr.file_source(gr.sizeof_short*1, "/home/martin/hrpt/baseband/METEOR-M-1/2011/07/24/METEOR-M-1_2011-07-24T113448_U2d50.sam", False)
		self.gr_file_sink_0_0_0 = gr.file_sink(gr.sizeof_char*1, "frames.mn1")
		self.gr_file_sink_0_0_0.set_unbuffered(False)
		self.gr_clock_recovery_mm_xx_0 = gr.clock_recovery_mm_ff(sps/2.0, clock_alpha**2/4.0, 0.5, clock_alpha, max_clock_offset)
		self.gr_binary_slicer_fb_0 = gr.binary_slicer_fb()
		self.gr_agc_xx_0_0 = gr.agc_cc(10e-6, 1, 1.0/32767.0, 1.0)
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
		self._decim_tb_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.decim_tb,
			callback=self.set_decim_tb,
			label="Decimation",
			converter=forms.int_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._decim_tb_text_box, 1, 3, 1, 1)
		self._datetime_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(3).GetWin(),
			value=self.datetime_text,
			callback=self.set_datetime_text,
			label="Local time of aquisition start",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(3).GridAdd(self._datetime_text_static_text, 1, 0, 1, 1)
		self.cs2cf = gr.interleaved_short_to_complex()
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
		self.connect((self.gr_throttle_0, 0), (self.cs2cf, 0))
		self.connect((self.pll, 0), (self.gr_moving_average_xx_0, 0))
		self.connect((self.gr_moving_average_xx_0, 0), (self.gr_clock_recovery_mm_xx_0, 0))
		self.connect((self.cs2cf, 0), (self.gr_agc_xx_0_0, 0))
		self.connect((self.gr_agc_xx_0_0, 0), (self.pll, 0))
		self.connect((self.cs2cf, 0), (self.wxgui_fftsink1, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.gr_binary_slicer_fb_0, 0))
		self.connect((self.gr_clock_recovery_mm_xx_0, 0), (self.gr_multiply_const_vxx_0, 0))
		self.connect((self.poesweather_meteor_cadu_deframer_0, 0), (self.gr_file_sink_0_0_0, 0))
		self.connect((self.gr_binary_slicer_fb_0, 0), (self.poesweather_meteor_cadu_deframer_0, 0))
		self.connect((self.gr_file_source_0_0, 0), (self.gr_throttle_0, 0))
		self.connect((self.gr_clock_recovery_mm_xx_0, 0), (self.wxgui_scopesink2_0, 0))

	def get_decim(self):
		return self.decim

	def set_decim(self, decim):
		self.decim = decim
		self.set_decim_tb(self.decim)

	def get_satellite(self):
		return self.satellite

	def set_satellite(self, satellite):
		self.satellite = satellite
		self.set_satellite_text(self.satellite)

	def get_frames_file(self):
		return self.frames_file

	def set_frames_file(self, frames_file):
		self.frames_file = frames_file
		self.set_frames_file_text_inf(self.frames_file)

	def get_baseband_file(self):
		return self.baseband_file

	def set_baseband_file(self, baseband_file):
		self.baseband_file = baseband_file
		self.set_baseband_file_text_inf(self.baseband_file)

	def get_symb_rate(self):
		return self.symb_rate

	def set_symb_rate(self, symb_rate):
		self.symb_rate = symb_rate
		self.set_symb_rate_tb(self.symb_rate)

	def get_clock_alpha(self):
		return self.clock_alpha

	def set_clock_alpha(self, clock_alpha):
		self.clock_alpha = clock_alpha
		self.set_clock_alpha_sl(self.clock_alpha)
		self.gr_clock_recovery_mm_xx_0.set_gain_omega(self.clock_alpha**2/4.0)
		self.gr_clock_recovery_mm_xx_0.set_gain_mu(self.clock_alpha)

	def get_pll_alpha(self):
		return self.pll_alpha

	def set_pll_alpha(self, pll_alpha):
		self.pll_alpha = pll_alpha
		self.set_pll_alpha_sl(self.pll_alpha)
		self.pll.set_alpha(self.pll_alpha)
		self.pll.set_beta(self.pll_alpha**2/4.0)

	def get_deframer_outsync_frames(self):
		return self.deframer_outsync_frames

	def set_deframer_outsync_frames(self, deframer_outsync_frames):
		self.deframer_outsync_frames = deframer_outsync_frames
		self.set_deframer_nosync_after_text(self.deframer_outsync_frames)

	def get_deframer_insync_frames(self):
		return self.deframer_insync_frames

	def set_deframer_insync_frames(self, deframer_insync_frames):
		self.deframer_insync_frames = deframer_insync_frames
		self.set_deframer_sync_after_text(self.deframer_insync_frames)

	def get_deframer_sync_check(self):
		return self.deframer_sync_check

	def set_deframer_sync_check(self, deframer_sync_check):
		self.deframer_sync_check = deframer_sync_check
		self.set_deframer_check_sync_text(self.deframer_sync_check)

	def get_decim_tb(self):
		return self.decim_tb

	def set_decim_tb(self, decim_tb):
		self.decim_tb = decim_tb
		self.set_samp_rate(100e6/self.decim_tb)
		self._decim_tb_text_box.set_value(self.decim_tb)

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
		self.set_samp_rate_st(self.samp_rate)
		self.set_sps(self.samp_rate/self.symb_rate_tb)
		self.set_max_carrier_offset(2*math.pi*100e3/self.samp_rate)
		self.wxgui_fftsink1.set_sample_rate(self.samp_rate)
		self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)

	def get_sps(self):
		return self.sps

	def set_sps(self, sps):
		self.sps = sps
		self.set_hs(int(self.sps/2.0))
		self.gr_clock_recovery_mm_xx_0.set_omega(self.sps/2.0)

	def get_v(self):
		return self.v

	def set_v(self, v):
		self.v = v
		self._v_check_box.set_value(self.v)

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

	def get_baseband_file_text_inf(self):
		return self.baseband_file_text_inf

	def set_baseband_file_text_inf(self, baseband_file_text_inf):
		self.baseband_file_text_inf = baseband_file_text_inf
		self._baseband_file_text_inf_static_text.set_value(self.baseband_file_text_inf)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("", "--decim", dest="decim", type="intx", default=50,
		help="Set Decimation [default=%default]")
	parser.add_option("", "--satellite", dest="satellite", type="string", default='Meteor-M-N1',
		help="Set Satellite [default=%default]")
	parser.add_option("", "--frames-file", dest="frames_file", type="string", default=os.environ['HOME'] + '/MN1_hrpt_frames.hmf',
		help="Set hmf output filename [default=%default]")
	parser.add_option("", "--baseband-file", dest="baseband_file", type="string", default="/home/martin/GNURadioData/hrpt/baseband/HRPT_Meteor-M-N1_2011-02-27_09-30-46_UTC_U2_d50.sam",
		help="Set Baseband output filename [default=%default]")
	parser.add_option("", "--symb-rate", dest="symb_rate", type="eng_float", default=eng_notation.num_to_str(600*1109),
		help="Set Symbol rate [default=%default]")
	parser.add_option("", "--clock-alpha", dest="clock_alpha", type="eng_float", default=eng_notation.num_to_str(0.050),
		help="Set Clock alpha [default=%default]")
	parser.add_option("", "--pll-alpha", dest="pll_alpha", type="eng_float", default=eng_notation.num_to_str(0.05),
		help="Set PLL alpha [default=%default]")
	parser.add_option("", "--deframer-outsync-frames", dest="deframer_outsync_frames", type="intx", default=100,
		help="Set Count of invalid ASM's after which deframer go out of synced state [default=%default]")
	parser.add_option("", "--deframer-insync-frames", dest="deframer_insync_frames", type="intx", default=3,
		help="Set Count of valid ASM's after which deframer go in to synced state [default=%default]")
	parser.add_option("", "--deframer-sync-check", dest="deframer_sync_check", type="intx", default=False,
		help="Set Deframer synchronisation check active [default=%default]")
	(options, args) = parser.parse_args()
	tb = bb_rx_mn1_hrpt_fr(decim=options.decim, satellite=options.satellite, frames_file=options.frames_file, baseband_file=options.baseband_file, symb_rate=options.symb_rate, clock_alpha=options.clock_alpha, pll_alpha=options.pll_alpha, deframer_outsync_frames=options.deframer_outsync_frames, deframer_insync_frames=options.deframer_insync_frames, deframer_sync_check=options.deframer_sync_check)
	tb.Run(True)

